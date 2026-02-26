import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/nllb-200-distilled-600M"

# JSON file storage paths
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "translated_output.json")