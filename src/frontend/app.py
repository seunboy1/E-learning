import os

import streamlit as st
from htmlTemplates import css
from streamlit_chat import message
from helper import handle_userinput, get_uploaded_document, handle_useranswer


def main():
    st.set_page_config(page_title="Q-A-T Chatbot", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Store test_question_id
    if "test_question_id" not in st.session_state:
        st.session_state.test_question_id = None

    st.header("Q-A-T Chatbot :books:")
    message("Hello, what would you like to learn today?", is_user=False)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True
        )

        if st.button("Process"):
            with st.spinner("Processing documents..."):
                # upload document
                if pdf_docs:
                    _ = get_uploaded_document(pdf_docs)
                else:
                    st.error("Upload PDF first!!!")

        user_question = st.text_input("Ask a question about your research documents:")
        user_answer = st.text_input("Answer the test question:")

    if user_question:
        with st.spinner("Loading..."):
            handle_userinput(user_question, key="user_input")
    elif user_answer:
        with st.spinner("Loading..."):
            handle_useranswer(user_answer, key="user_answer")


if __name__ == "__main__":
    main()
