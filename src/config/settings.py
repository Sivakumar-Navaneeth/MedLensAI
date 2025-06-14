import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
MODEL_DIR = DATA_DIR / "models"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/medlensai")

# Model settings
MODEL_NAME = "google/medgemma-2b"
DEVICE = os.getenv("DEVICE", "cuda" if os.getenv("USE_GPU", "true").lower() == "true" else "cpu")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "dicom"}

# External API settings
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY")
WHO_ICD_API_KEY = os.getenv("WHO_ICD_API_KEY")
UMLS_API_KEY = os.getenv("UMLS_API_KEY")

# Model parameters
MAX_LENGTH = 512
TEMPERATURE = 0.7
TOP_P = 0.9
NUM_RETURN_SEQUENCES = 1 