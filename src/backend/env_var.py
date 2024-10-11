from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

class EnvVariable(Enum):
    DB_NAME = os.environ.get("DB_NAME")
    GCP_API_KEY = os.getenv("GCP_API_KEY")
    GCP_MODEL = os.environ.get("GCP_MODEL")
    FAISS_PATH = os.environ.get("FAISS_PATH")
    BACKEND_URL = os.environ.get("BACKEND_URL")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    HUGGINFACEHUB_API_TOKEN = os.environ.get("HUGGINFACEHUB_API_TOKEN")