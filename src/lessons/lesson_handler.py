"""
Module for handling lessons
"""
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lessons.lesson_content import get_lesson_by_id, get_lesson_by_topic, LESSONS
from src.gamification.xp_system import award_xp, get_user_level

# Create a router
router = Router()

# Define states for the lesson flow
class LessonStates(StatesGroup):
    viewing_theory = State()
    answering_questions = State()
    completed = State()

# Store user lesson data in memory (in a real app, this would be in a database)
user_lesson_data = {}

@router.message(Command("lesson"))
async def cmd_start_lesson(message: Message, state: FSMContext):
    """
    Start or continue a lesson
    """
    user_id = message.from_user.id
    
    # In a real app, we would check the database to see which lesson the user should take next
    # For now, we'll just start with the first lesson if they haven't started any,
    # or continue from where they left off
    
    if user_id not in user_lesson_data:
        # New user, start with lesson 1
        current_lesson_id = 1
        user_lesson_data[user_id] = {
            "current_lesson": current_lesson_id,
            "last_lesson_date": datetime.now(),
            "completed_lessons": []
        }
    else:
        # Check if 24 hours have passed since the last lesson
        last_lesson_date = user_lesson_data[user_id]["last_lesson_date"]
        time_since_last_lesson = datetime.now() - last_lesson_date
        
        if time_since_last_lesson < timedelta(hours=24) and user_lesson_data[user_id]["current_lesson"] in user_lesson_data[user_id]["completed_lessons"]:
            # Less than 24 hours and current lesson completed, tell user to wait
            hours_to_wait = 24 - (time_since_last_lesson.total_seconds() / 3600)
            await message.answer(
                f"Вы уже прошли урок сегодня! Следующий урок будет доступен через {int(hours_to_wait)} часов.\n\n"
                f"Пока вы ждете, почему бы не повторить пройденный материал?"
            )
            return
        
        # Get the current lesson or move to the next one if completed
        if user_lesson_data[user_id]["current_lesson"] in user_lesson_data[user_id]["completed_lessons"]:
            # Move to the next lesson
            current_lesson_id = user_lesson_data[user_id]["current_lesson"] + 1
            if current_lesson_id > len(LESSONS):
                # All lessons completed
                await message.answer(
                    "Поздравляем! Вы прошли все уроки в нашем курсе. 🎉\n\n"
                    "Скоро мы добавим новые уроки. А пока вы можете повторить пройденный материал с помощью команды /review."
                )
                return
            
            user_lesson_data[user_id]["current_lesson"] = current_lesson_id
            user_lesson_data[user_id]["last_lesson_date"] = datetime.now()
        else:
            # Continue with the current lesson
            current_lesson_id = user_lesson_data[user_id]["current_lesson"]
    
    # Get the lesson content
    lesson = get_lesson_by_id(current_lesson_id)
    if not lesson:
        await message.answer("Урок не найден. Пожалуйста, свяжитесь с администратором.")
        return
    
    # Set state to viewing theory
    await state.set_state(LessonStates.viewing_theory)
    
    # Create keyboard
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти к практике", callback_data=f"practice_{current_lesson_id}")
    
    # Send lesson theory
    await message.answer(
        f"<b>Урок {current_lesson_id}: {lesson['topic']}</b>\n\n"
        f"{lesson['theory']}\n\n"
        f"<code>{lesson['code_example']}</code>\n\n"
        f"Когда будете готовы, переходите к практическим заданиям.",
        reply_markup=builder.as_markup()
    )
    
    # Award XP for viewing theory
    await award_xp(user_id, 10, "Просмотр теории")

@router.callback_query(F.data.startswith("practice_"))
async def start_practice(callback: CallbackQuery, state: FSMContext):
    """
    Start the practice part of the lesson
    """
    await callback.answer()
    
    user_id = callback.from_user.id
    lesson_id = int(callback.data.split("_")[1])
    
    # Get the lesson content
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        await callback.message.answer("Урок не найден. Пожалуйста, свяжитесь с администратором.")
        return
    
    # Set state to answering questions
    await state.set_state(LessonStates.answering_questions)
    
    # Store question data
    await state.update_data(
        lesson_id=lesson_id,
        questions=lesson["questions"],
        current_question=0,
        correct_answers=0
    )
    
    # Send the first question
    await send_question(callback.message, state)

async def send_question(message: Message, state: FSMContext):
    """
    Send a practice question to the user
    """
    # Get question data
    data = await state.get_data()
    current_idx = data["current_question"]
    questions = data["questions"]
    
    if current_idx >= len(questions):
        # No more questions, finish the practice
        await finish_practice(message, state)
        return
    
    question = questions[current_idx]
    
    # Create keyboard with options
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(question["options"]):
        builder.button(text=option, callback_data=f"option_{i}")
    
    # Send question
    await message.answer(
        f"Вопрос {current_idx + 1} из {len(questions)}:\n\n"
        f"{question['text']}",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("option_"))
async def process_practice_answer(callback: CallbackQuery, state: FSMContext):
    """
    Process the user's answer to a practice question
    """
    await callback.answer()
    
    # Get selected option
    selected_option = int(callback.data.split("_")[1])
    
    # Get question data
    data = await state.get_data()
    current_idx = data["current_question"]
    questions = data["questions"]
    question = questions[current_idx]
    
    # Check if the answer is correct
    is_correct = selected_option == question["correct_index"]
    
    # Update correct answer count
    if is_correct:
        data["correct_answers"] += 1
        await award_xp(callback.from_user.id, 20, "Правильный ответ")
    
    # Move to the next question
    data["current_question"] += 1
    await state.update_data(data)
    
    # Send feedback
    if is_correct:
        await callback.message.answer("✅ Правильно!")
    else:
        correct_option = question["options"][question["correct_index"]]
        await callback.message.answer(f"❌ Неправильно. Правильный ответ: {correct_option}")
    
    # Send the next question
    await send_question(callback.message, state)

async def finish_practice(message: Message, state: FSMContext):
    """
    Finish the practice part of the lesson
    """
    # Get lesson data
    data = await state.get_data()
    lesson_id = data["lesson_id"]
    correct_answers = data["correct_answers"]
    total_questions = len(data["questions"])
    
    # Calculate score
    score_percentage = (correct_answers / total_questions) * 100
    
    # Mark lesson as completed
    user_id = message.chat.id
    if user_id in user_lesson_data:
        if lesson_id not in user_lesson_data[user_id]["completed_lessons"]:
            user_lesson_data[user_id]["completed_lessons"].append(lesson_id)
            # Award XP for completing the lesson
            await award_xp(user_id, 50, "Завершение урока")
    
    # Get user level
    level = await get_user_level(user_id)
    
    # Create keyboard for sharing
    builder = InlineKeyboardBuilder()
    builder.button(text="Поделиться прогрессом", callback_data=f"share_{lesson_id}")
    
    # Send completion message
    await message.answer(
        f"🎉 Урок {lesson_id} завершен!\n\n"
        f"Ваш результат: {correct_answers} из {total_questions} ({score_percentage:.1f}%)\n\n"
        f"Вы заработали XP и достигли уровня {level}!\n\n"
        f"Следующий урок будет доступен через 24 часа. Не забудьте вернуться завтра!",
        reply_markup=builder.as_markup()
    )
    
    # Reset state
    await state.clear()