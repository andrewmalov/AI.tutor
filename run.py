"""
Script to run the bot
"""
import asyncio
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    """Main function"""
    # Load environment variables
    load_dotenv()
    
    # Check if BOT_TOKEN is set
    if not os.getenv("BOT_TOKEN"):
        logger.error("BOT_TOKEN is not set in .env file")
        print("Error: BOT_TOKEN is not set in .env file")
        print("Please create a .env file with your Telegram bot token:")
        print("BOT_TOKEN=your_telegram_bot_token_here")
        return
    
    # Import and run the bot
    from main import main as run_bot
    await run_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")