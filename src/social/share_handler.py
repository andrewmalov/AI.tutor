"""
Module for handling social media sharing
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import tempfile

from src.social.share_generator import generate_share_image
from src.gamification.xp_system import user_xp_data, award_achievement

# Create a router
router = Router()

# Store user share count (in a real app, this would be in a database)
user_shares = {}

@router.callback_query(F.data.startswith("share_"))
async def share_progress(callback: CallbackQuery):
    """
    Handle the share progress button
    """
    await callback.answer()
    
    user_id = callback.from_user.id
    lesson_id = int(callback.data.split("_")[1])
    
    # Get user data
    if user_id not in user_xp_data:
        await callback.message.answer("Произошла ошибка. Пожалуйста, начните обучение заново.")
        return
    
    user_data = user_xp_data[user_id]
    
    # Generate share image
    image_bio = await generate_share_image(user_data)
    
    # Save image to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(image_bio.getvalue())
        temp_file_path = temp_file.name
    
    # Send image to user
    await callback.message.answer_photo(
        FSInputFile(temp_file_path),
        caption=(
            f"🚀 Я на уровне {user_data['level']} в Python Tutor Bot!\n"
            f"Пройдено уроков: {len(user_data.get('completed_lessons', []))}\n"
            f"Дней подряд: {user_data['streak_days']}\n\n"
            f"Присоединяйся к обучению! t.me/your_bot_username"
        )
    )
    
    # Create keyboard with share buttons
    builder = InlineKeyboardBuilder()
    builder.button(text="Поделиться в Twitter", url="https://twitter.com/intent/tweet?text=Я+учу+Python+с+Python+Tutor+Bot!+t.me/your_bot_username")
    builder.button(text="Поделиться в Facebook", url="https://www.facebook.com/sharer/sharer.php?u=t.me/your_bot_username")
    
    await callback.message.answer(
        "Поделитесь своим прогрессом в социальных сетях!",
        reply_markup=builder.as_markup()
    )
    
    # Clean up temporary file
    os.unlink(temp_file_path)
    
    # Track share count
    if user_id not in user_shares:
        user_shares[user_id] = 1
    else:
        user_shares[user_id] += 1
    
    # Check for social butterfly achievement
    if user_shares[user_id] == 3:
        await award_achievement(user_id, "social_butterfly", "Социальная бабочка", "Вы поделились своим прогрессом 3 раза!")