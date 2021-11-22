import os
from dotenv import load_dotenv

from bot import bot

if __name__ == "__main__":
    ENV = os.getenv("ENV")
    
    if ENV == 'dev':
        load_dotenv('.env.dev')
    else:
        load_dotenv('.env')
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
