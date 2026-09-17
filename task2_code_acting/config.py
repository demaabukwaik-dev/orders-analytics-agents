import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HF_TOKEN")

MODEL_NAME = "Qwen/Qwen3-Coder-Next"
BASE_URL = "https://router.huggingface.co/v1"


CSV_PATH = "data/order_processing_agent_50_orders.csv"


