# E-learning Chatbot

## Overview

The E-learning System (Question, Answer & Test) is an intelligent document-based Q&A solution designed to facilitate enhanced user interaction with research documents. Unlike traditional Q&A systems that simply return an answer to a user’s question, the E-learning system extends this process by including a "test question" in its response. This test question is used to evaluate whether the user understood the provided answer, promoting deeper engagement and learning. This system is ideal for users who want to better understand research documents and ensure they are grasping the material effectively.


## How it Works
- Upload Document: The system allows users to upload research documents (PDF). The content is extracted and stored in a way that can be queried later.
- Ask a Question: Users submit a question related to the uploaded document. The system processes the document and generates a detailed answer, followed by a test question.
- Test Users Knowledge: The system returns a test question along with the answer, designed to evaluate the user's understanding.
- Evaluate Response: Users respond to the test question, and the system evaluates the response, providing feedback and a score based on the quality of the answer.

---

## Project Structure

```bash
├── backend/
|   ├── env_var.py            # Handles the environmental variables used in this project
|   ├── app.py                # Entry point for FastAPI app
|   ├── helper.py             # Helper functions for the backend service
|   ├── database.py           # Contains the encapsulated class for communicated with the database
├── frontend/
|   ├── app.py                # Entry point for Streamlit app
|   ├── helper.py             # Helper functions for the frontend service
|   ├── env_var.py            # Handles the environmental variables used in this project
├── vector/                   # vector database directory
├── .env                      # Contains the environmental variables used in this project
├── .gitignore
├── .pre-commit-config.yaml   # Configuration file for the pre commit hook
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview (this file)# Mastery-hive-assesment -->
```

### Installation

- Install python 3.9
    ```bash
        # Using Ubuntu/Debian:
        sudo apt update
        sudo apt install python3.9
        sudo apt install python3.9-venv

        # Using MacOS
        brew install python@3.9
    ```
- Create and activate virtual environment to manage dependencies:
    ```bash
        make activate 
    ```
    
- Install necessary libraries:
    ```bash
        make install 
    ```
    
    
- To perform testing, test coverage, code formatting, linting

    - Manually, run the following:
        - Code formatting
            ```bash
                make format 
            ```

        - Linting
            ```bash
                make lint 
            ```

        - Testing and test ccoverage
            ```bash
                make test 
            ```

    - Automatically:
        - Use pre commit hook
            ```bash
                pre-commit install
            ```
        - Now commit and push your code
            ```bash
                git add *
                git commit -m "your_message"
                git push 
            ```
        - Now you can make changes and commit. It should return something like this:

            ![result](./docs/result.png)
    
- LLM 
  - To use Open AI(this is not free). [Link](https://platform.openai.com/docs/quickstart)
    ```
        Go to Open AI website to generate a Key
    ```

  - Generate an API_KEY [GEMINI PRO](https://ai.google.dev/gemini-api/docs/api-key) and [HUGGING FACE](https://www.nightfall.ai/ai-security-101/hugging-face-api-key)

    ```
        Go to Google  website to generate a Key
        Go to Hugging face  website to generate a Key
    ```

API_KEY = "YOUR_API_KEY"
- Set up environment variables by creating a `.env` file:
    ```env
        FAISS_PATH=<path_to_faiss>
        OPENAI_API_KEY=<your_openai_api_key>
        HUGGINFACEHUB_API_TOKEN=<huggingface_api_token>
        BACKEND_URL=http://127.0.0.1:5000
        GCP_MODEL=gemini-pro
        DB_NAME=yourdatabsename.db
        GCP_API_KEY=<your_gcp_api_key>
        HUGGINFACEHUB_API_TOKEN=<your_huggingface_api_key>
    ```

- Run backend:
    ```bash
        python backend/app.py
    ```

- Run frontend:
    ```bash
        streamlit run frontend/app.py
    ```

- Open `http://localhost:8501` in your browser to interact with the chatbot.


-  Access the Application
    - Frontend (Streamlit): Open your browser and navigate to http://localhost:8501
    - Backend (FLASK): The backend API is accessible at http://localhost:5000

