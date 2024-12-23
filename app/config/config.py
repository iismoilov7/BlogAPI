import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

ENV = os.getenv("ENV", "dev")
DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC")
BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')))
JWT_ALGORITHM = "HS256"
JWT_PRIVATE_KEY_PATH = BASE_DIR / "certs" / "jwt-private.pem"
JWT_PUBLIC_KEY_PATH = BASE_DIR / "certs" / "jwt-public.pem"
ACCESS_TOKEN_EXPIRES_MINUTES = timedelta(days=7)
SALT = os.getenv("SALT")

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
