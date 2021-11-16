import os
from dotenv import load_dotenv

from bot import bot

if __name__ == "__main__":
	load_dotenv()
	TOKEN = os.getenv('BOT_TOKEN')
	bot.run(TOKEN)