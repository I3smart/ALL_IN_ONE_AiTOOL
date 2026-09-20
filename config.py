import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OWNER_IDS = [int(x.strip()) for x in os.getenv("OWNER_IDS", "").split(",") if x.strip()]
OWNER_USERNAMES = os.getenv("OWNER_USERNAMES", "@nepoliyan_heart_147, @ISUZI_ENGINE")

SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "@ai_support_147")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "@all_in_1_ai")

FREE_TRIAL_LIMIT = int(os.getenv("FREE_TRIAL_LIMIT", "3"))
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")
