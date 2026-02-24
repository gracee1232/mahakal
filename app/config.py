import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/nllb-200-distilled-600M"