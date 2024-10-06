from enum import Enum
from dotenv import load_dotenv
import os


load_dotenv()

class EnvVariable(Enum):
    FAISS_PATH = os.environ.get("FAISS_PATH")
    BACKEND_URL = os.environ.get("BACKEND_URL")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    HUGGINFACEHUB_API_TOKEN = os.environ.get("HUGGINFACEHUB_API_TOKEN")