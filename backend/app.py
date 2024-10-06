import os
from env_var import EnvVariable
from database import Database
from flask import Flask, request, jsonify, session
from helper import get_pdf_text, get_text_chunks, get_vectorstore, query, get_pdf_text_from_path, evaluate_with_llm


app = Flask(__name__)

# Set your secret key here. It can be any random string.
DB_NAME = EnvVariable.DB_NAME.value

# Initialize the database interaction
db = Database(DB_NAME)

@app.before_request
def initialize_database():
    """Initialize the database when the application starts."""
    db.init_db()

@app.teardown_appcontext
def close_database(exception):
    """Close the database connection after each request."""
    db.close_db()

# Endpoint to upload the research document
@app.route('/upload/', methods=['POST'])
def upload_document():

    # Check if files are provided in the request
    if 'pdf_doc_0' in request.files:
        # Get the PDF files from the request
        pdf_docs = request.files.to_dict()
        # Extract text from the PDF files
        raw_text = get_pdf_text(pdf_docs)
    elif 'file_paths' in request.json:
        file_paths = request.json.get('file_paths', [])
              
        # Ensure file paths are valid
        for file_path in file_paths:
            if not os.path.exists(file_path):
                return {'error': f"File {file_path} does not exist"}, 400
        # Extract text from the provided file paths
        raw_text = get_pdf_text_from_path(file_paths)
    else:
        return {'error': 'No files or file paths provided'}, 400

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    # Specify a path to save the FAISS index
    index_path = EnvVariable.FAISS_PATH.value
    vectorstore.save_local(index_path)

    # return jsonify({'message': 'Document uploaded successfully', 'vectorstore': vectorstore}), 201
    return jsonify({'message': 'Document uploaded successfully'}), 201

# Endpoint to query the system and get an answer with test question
@app.route('/query/', methods=['POST'])
def query_document():
    user_input = request.json.get("question")

    # Call function to get answer, test question, and bullet points
    response = query(user_input)

    # Save test question and answer to the database
    db.save_test_question(
        response['test_question_id'],
        response['test_question'],
        response['test_answer']
    )

    # Return the required JSON response
    return jsonify({
        "answer": response['answer'],
        "bullet_points": response['bullet_points'],
        "test_question": response['test_question'],
        "test_answer": response['test_answer'],
        "test_question_id": response['test_question_id']
    })

@app.route('/evaluate/', methods=['POST'])
def evaluate():
    try:
        # Extract data from the incoming request
        user_answer = request.json.get("answer")
        test_question_id = request.json.get("test_question_id")

        # Validate input
        if not user_answer or not test_question_id:
            return jsonify({"error": "Missing required fields: 'answer' and 'test_question_id'"}), 400

        # Fetch the correct answer from the database
        test_answer = db.get_test_answer(test_question_id)
        if not test_answer:
            return jsonify({"error": "Test question not found"}), 404
        test_question = db.get_test_question(test_question_id)

        # Call the evaluation function
        evaluation_result = evaluate_with_llm(test_question, user_answer, test_answer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(evaluation_result)

@app.route('/')
def health_check():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=False)