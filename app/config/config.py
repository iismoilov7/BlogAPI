from os import getenv
from dotenv import load_dotenv

load_dotenv()

ENV = getenv("ENV", "dev")

# Configure CORS origins based on the environment
if ENV == "dev":
    ORIGINS = ["*"]  # Allow all origins in development
    HOST = "127.0.0.1"
    DEBUG = True
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    PORT = 7777
else:
    ORIGINS = [
        "https://ismoil.site/"  # Add your specific frontend origin
    ]
    HOST = "0.0.0.0"
    DEBUG = False
    DOCS_URL = None
    REDOC_URL = None
    PORT = 8000
