import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "health_log.csv")