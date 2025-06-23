"""
Main application file for Python Tutor Bot
"""
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.database.db import init_db
from src.lessons.test_handler import router as test_router
from src.lessons.lesson_handler import router as lesson_router
from src.social.share_handler import router as share_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Register routers
dp.include_router(test_router)
dp.include_router(lesson_router)
dp.include_router(share_router)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Handle the /start command - entry point of the bot
    """
    await message.answer(
        "Привет! Я помогу тебе выучить Python играючи. "
        "Пройди быстрый тест из 10 вопросов, чтобы начать!\n\n"
        "Используй команду /test для начала тестирования."
    )

@dp.message(lambda message: message.text == "/help")
async def help_handler(message: Message) -> None:
    """
    Handle the /help command
    """
    await message.answer(
        "Python Tutor Bot - ваш персональный помощник в изучении Python.\n\n"
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/test - Пройти диагностический тест\n"
        "/lesson - Начать или продолжить урок\n"
        "/progress - Посмотреть свой прогресс\n"
        "/help - Показать это сообщение\n\n"
        "Как это работает:\n"
        "1. Пройдите тест для определения ваших слабых мест\n"
        "2. Получите персонализированный план обучения\n"
        "3. Проходите ежедневные уроки и зарабатывайте XP\n"
        "4. Делитесь своими достижениями с друзьями"
    )

@dp.message(lambda message: message.text == "/progress")
async def progress_handler(message: Message) -> None:
    """
    Handle the /progress command
    """
    from src.gamification.xp_system import user_xp_data
    
    user_id = message.from_user.id
    
    if user_id not in user_xp_data:
        await message.answer(
            "У вас пока нет прогресса. Начните обучение с команды /test!"
        )
        return
    
    user_data = user_xp_data[user_id]
    
    # Format achievements
    achievements_text = "Нет достижений"
    if user_data.get("achievements"):
        achievements_text = "\n".join([f"• {a['name']} - {a['description']}" for a in user_data["achievements"]])
    
    # Format completed lessons
    completed_lessons = user_data.get("completed_lessons", [])
    lessons_text = "Нет пройденных уроков"
    if completed_lessons:
        from src.lessons.lesson_content import get_lesson_by_id
        lessons_text = "\n".join([f"• Урок {lesson_id}: {get_lesson_by_id(lesson_id)['topic']}" for lesson_id in completed_lessons])
    
    await message.answer(
        f"📊 Ваш прогресс:\n\n"
        f"Уровень: {user_data['level']}\n"
        f"XP: {user_data['xp']}\n"
        f"Дней подряд: {user_data['streak_days']}\n\n"
        f"🏆 Достижения:\n{achievements_text}\n\n"
        f"📚 Пройденные уроки:\n{lessons_text}"
    )

async def main() -> None:
    """
    Main function to start the bot
    """
    # Initialize database
    await init_db()
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot_instance = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    
    # Start polling
    await dp.start_polling(bot_instance)

if __name__ == "__main__":
    asyncio.run(main())