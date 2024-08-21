from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = getenv("BOT_TOKEN")

if not TOKEN:
    print("ERROR: Not bot token in env ('BOT_TOKEN=xxx')'")
    exit()
