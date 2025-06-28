import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly specify the .env file path if needed

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")