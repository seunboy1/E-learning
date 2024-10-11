import os
import requests
import faiss
import streamlit as st
from env_var import EnvVariable
from streamlit_chat import message
from htmlTemplates import bot_template, user_template


backend_url = os.getenv("BACKEND_URL")


def generate_answer_and_test_question(user_question, session_state):
    """
    Main function that returns answer to the user question
    """
    payload = {"user_message": user_question, "session_state": session_state}

    # Make POST request to FastAPI backend
    response, status_code = requests.post(
        f"{backend_url}/chat/", json=payload, timeout=20
    )
    return response.json()


def get_uploaded_document(pdf_docs):
    files = {}
    if pdf_docs:
        for i, pdf in enumerate(pdf_docs):
            # Add each PDF file to the files dictionary
            files[f"pdf_doc_{i}"] = (pdf.name, pdf.getvalue(), "application/pdf")
        # Send the POST request with files
        response = requests.post(f"{backend_url}/upload/", files=files, timeout=60)

        # Get the response in JSON format
    return response.json()


def handle_userinput(user_question, key="user_input"):

    payload = {"question": user_question}
    response = requests.post(f"{backend_url}/query/", json=payload)
    answer = response.json().get("answer")

    message(user_question, is_user=True, key=f"{key}_user_message")

    st.markdown("Answer: ")
    message(answer, is_user=False, key=f"{key}_response_message")

    # Display bullet points
    st.markdown("Bullet Points: ")
    bullet_points = response.json().get("bullet_points")
    bullet_point_str = "\n".join([f"• {point}" for point in bullet_points])
    message(f"{bullet_point_str}", is_user=False, key=f"{key}_bullet_points")

    # Display the generated test question
    st.markdown("Test Question: ")
    test_question = response.json().get("test_question")
    message(f"{test_question}", is_user=False, key=f"{key}_test_question")

    st.session_state.test_question_id = response.json().get("test_question_id")


def handle_useranswer(user_answer, key="user_answer"):
    payload = {
        "answer": user_answer,
        "test_question_id": st.session_state.test_question_id,
    }
    response = requests.post(f"{backend_url}/evaluate/", json=payload)
    message(user_answer, is_user=True, key=f"{key}_user_answer")

    st.markdown("Knowledge Understood: ")
    knowledge_understood = response.json().get("knowledge_understood")
    message(str(knowledge_understood), is_user=False, key=f"{key}_knowledge_understood")

    st.markdown("Knowledge Confidence: ")
    knowledge_confidence = response.json().get("knowledge_confidence")
    message(str(knowledge_confidence), is_user=False, key=f"{key}_knowledge_confidence")
