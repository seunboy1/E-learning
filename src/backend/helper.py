import os
import uuid
import sqlite3
from PyPDF2 import PdfReader
from env_var import EnvVariable
from operator import itemgetter
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings


# environment variable inititalization
FAISS_PATH = EnvVariable.FAISS_PATH.value
GCP_MODEL = EnvVariable.GCP_MODEL.value
GCP_API_KEY = EnvVariable.GCP_API_KEY.value
OPENAI_API_KEY = EnvVariable.OPENAI_API_KEY.value

# Initialize global variables
if OPENAI_API_KEY:
    llm = ChatOpenAI()
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
elif GCP_API_KEY:
    # Initialize LangChain LLM with GCP Gemini Pro
    llm = ChatGoogleGenerativeAI(model=GCP_MODEL, google_api_key=GCP_API_KEY)
    embeddings = HuggingFaceEmbeddings()

vectorstore_path = EnvVariable.FAISS_PATH.value

if os.path.exists(vectorstore_path):
    vector_store = FAISS.load_local(
        vectorstore_path, embeddings, allow_dangerous_deserialization=True
    )
else:
    vector_store = None


# Function to extract text from PDF
def get_pdf_text(pdf_docs):
    text = ""
    for key, pdf in pdf_docs.items():
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# Function to extract text from a file path
def get_pdf_text_from_path(file_paths):
    text = ""
    for file_path in file_paths:
        with open(file_path, "rb") as f:
            pdf_reader = PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def generate_answer():
    answer_prompt_template = """
    
        You are a highly knowledgeable and versatile AI assistant designed to provide thorough, detailed, and easy-to-understand explanations. nswer the question based only on the information provided for you in the context
        context:
        {context}
        Follow these rules:
        
        - Provide an elaborate answer based on the provided documents and context.
        - Break down the solution into simple terms and technical details so both a beginner and an expert can understand.
        - Include relevant examples or comparisons where necessary to enhance understanding.
        - Explain every list item, bullet points clearly
        - Summarize key points at the end of the answer.
        - Use a friendly and engaging tone, but avoid informal language and emoticons.
        - If the provided text does not contain the answer, state that the answer is not available based on the current data.
        
        Question:  {question}
    """
    answer_template = PromptTemplate(
        template=answer_prompt_template,
        input_variables=["question"],
    )

    answer_chain = answer_template | llm | StrOutputParser()
    return answer_chain


def generate_test_question_and_answer():
    # Create a structured prompt to generate both the test question and answer in one go
    question_prompt_template = """
        You are a multi-purpose bot whose job is to generate exam-standard questions. Using the information from the 
        context, Question and the answer provided below, generate a specific test question and answer to evaluate the 
        user's understanding of the topic.
        
        Question: {question}

        Context: {context}

        Answer: {answer}
        Follow these rules:
        - The test question should start with one of the following formats:
            1. "What are..." for lists, definitions, or components.
            2. "How many..." for numerical or count-based questions.
            3. "What is the best way..." for advice, processes, or recommendations.
        - Ensure the generated question directly relates to the answer provided.
        - After generating the test question, provide a detailed and clear answer to the question.
        - The response should consist of exactly two sentences seperated ny fullstop: the first is the test question, and the second is the answer 
        - Ensure the question and answer follow exam-standard formats and provide useful information.
        - No emojis or emoticons should be returned in your response.
    """
    test_question_template = PromptTemplate(
        template=question_prompt_template,
        input_variables=["context", "question", "answer"],
    )
    test_question_chain = test_question_template | llm | StrOutputParser()

    return test_question_chain


def generate_bullet_points():

    # Create a structured prompt for the model
    bullet_point_prompt_template = """
        You are a multi-purpose bot whose one job is to engage the user. 
        Follow these rules:
        - From the question, answer and context provided, generate a list of bullet points emphasizing key details in the answer to improve
        understanding, seperated by fullstops
        - This should be concise and be a summary of the answer
        - Use an enthusiastic and engaging tone to keep the user engaged.
        - No emojis or emoticons should be returned in your response.
        - Return just the list 

        Question:  {question}

        context: {context}

        answer: {answer}
    """
    bullet_template = PromptTemplate(
        template=bullet_point_prompt_template,
        input_variables=["context", "question", "answer"],
    )
    bullet_chain = bullet_template | llm | StrOutputParser()

    return bullet_chain


def generate_test_question_id():
    """
    Generates a unique test_question_id using UUID.

    Returns:
        str: A unique test_question_id in string format.
    """
    return str(uuid.uuid4())


def query(user_input):
    # Tell Python to use the global vector_store
    global vector_store
    if vector_store is None:
        vector_store = FAISS.load_local(
            vectorstore_path, embeddings, allow_dangerous_deserialization=True
        )

    # Generate unique id
    test_question_id = generate_test_question_id()

    # Extract the main answer from the response
    answer_chain = generate_answer()

    # Generate a test question based on the main answer
    test_question_chain = generate_test_question_and_answer()

    # Generate bullet points
    bullet_chain = generate_bullet_points()

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 4})
    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
        }
        | RunnablePassthrough.assign(answer=answer_chain)
        | RunnablePassthrough.assign(test_question=test_question_chain)
        | RunnablePassthrough.assign(bullet_points=bullet_chain)
    )

    response = chain.invoke({"question": user_input})

    bullet_points = response["bullet_points"].split("-\n")
    test_question = response["test_question"].split("?")[0]
    test_answer = response["test_question"].split("?")[1].strip()

    # Return the response along with the bullet points, test question, and test question ID
    return {
        "answer": response["answer"],
        "bullet_points": bullet_points,
        "test_answer": test_answer,
        "test_question": test_question,
        "test_question_id": test_question_id,
    }


# Function to evaluate the answer using LLM
def evaluate_with_llm(question: str, user_answer: str, correct_answer: str) -> dict:
    """Evaluates whether the user understood the question and gives a confidence score using LLM."""

    evaluation_template = """
    You are given a question and two answers (one correct and one user's). Determine if the user understands the topic based on their answer.
    
    Question: {question}
    
    Correct Answer: {correct_answer}
    
    User's Answer: {user_answer}
    
    Respond with 'True' if the user understands the topic and 'False' if they do not.
    """

    confidence_template = """
    You are given a question and two answers (one correct and one user's). Rate the user's confidence in their answer on a scale from 1 to 100, where 100 means complete understanding.
    Only give a confidence score in integer no explanation needed
    Question: {question}
    
    Correct Answer: {correct_answer}
    
    User's Answer: {user_answer}
    """

    # Prepare the prompts
    evaluation_prompt = PromptTemplate(
        template=evaluation_template,
        input_variables=["question", "correct_answer", "user_answer"],
    )
    confidence_prompt = PromptTemplate(
        template=confidence_template,
        input_variables=["question", "correct_answer", "user_answer"],
    )

    # Call the LLM for understanding evaluation
    evaluation_chain = evaluation_prompt | llm | StrOutputParser()
    evaluation_result = evaluation_chain.invoke(
        {
            "question": question,
            "correct_answer": correct_answer,
            "user_answer": user_answer,
        }
    )

    # Call the LLM for confidence evaluation
    confidence_chain = confidence_prompt | llm | StrOutputParser()
    confidence_result = confidence_chain.invoke(
        {
            "question": question,
            "correct_answer": correct_answer,
            "user_answer": user_answer,
        }
    )

    # Parse results
    knowledge_understood = evaluation_result.strip() == "True"
    knowledge_confidence = int(
        confidence_result.split(":")[-1]
    )  # Convert confidence to integer

    return {
        "knowledge_understood": knowledge_understood,
        # "question": question,
        # "correct_answer": correct_answer,
        "knowledge_confidence": knowledge_confidence,
    }
