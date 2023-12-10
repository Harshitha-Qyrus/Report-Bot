import os
from dotenv import load_dotenv

load_dotenv()

class OPENAI_CONFIG:
    AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT","https://qyrus-ai-east-us-2.openai.azure.com/")
    AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_KEY", "46861c43ff474f68b24dcde19c9314e5")
    AZURE_API_VERSION=os.environ.get("OPENAI_API_VERSION", "2023-07-01-preview")
    API_TYPE = os.environ.get("OPENAI_API_TYPE", "azure")
    OPENAI_RETRIES=int(os.environ.get("OPENAI_RETRIES",4))

    MODELS = {
        "text-embedding-ada-002": "textada002",
        "gpt-3.5-turbo-16k": "gpt3516k",
        "gpt-4": "gpt48k",
        "gpt-4-32k": "gpt432k"
    }

class DB_CONFIG:
    SSH_HOST = os.environ.get("DB_SSH_HOST")
    SSH_PKEY_FILE = os.environ.get("DB_SSH_PKEY_FILE")
    SSH_UNAME = os.environ.get("DB_SSH_UNAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_UNAME = os.environ.get("DB_UNAME")
    DB_PASS = os.environ.get("DB_PASS")