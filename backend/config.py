import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly specify the .env file path if needed

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI")
    GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")
    GOOGLE_CERT_URL = os.getenv("GOOGLE_CERT_URL")