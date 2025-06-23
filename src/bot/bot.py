import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Handle the /start command - entry point of the bot
    """
    await message.answer(
        "Привет! Я помогу тебе выучить Python играючи. "
        "Пройди быстрый тест из 10 вопросов, чтобы начать!"
    )
    # Here we'll add logic to start the diagnostic test

async def main() -> None:
    """
    Main function to start the bot
    """
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot_instance = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot_instance)

if __name__ == "__main__":
    asyncio.run(main())