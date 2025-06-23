"""
Module for handling the diagnostic test
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import User, TestResult
from src.lessons.test_questions import get_test_questions
from src.lessons.plan_generator import generate_learning_plan

# Create a router
router = Router()

# Define states for the test flow
class TestStates(StatesGroup):
    waiting_for_start = State()
    answering_questions = State()
    finished = State()

# Store user test data in memory (in a real app, this would be in a database)
user_test_data = {}

@router.message(Command("test"))
async def cmd_start_test(message: Message, state: FSMContext):
    """
    Start the diagnostic test
    """
    # Initialize test data for this user
    user_id = message.from_user.id
    questions = get_test_questions(10)  # Get 10 random questions
    
    user_test_data[user_id] = {
        "questions": questions,
        "current_question": 0,
        "answers": [],
        "category_scores": {
            "syntax": 0,
            "data_types": 0,
            "functions": 0,
            "loops": 0,
            "oop": 0
        },
        "category_counts": {
            "syntax": 0,
            "data_types": 0,
            "functions": 0,
            "loops": 0,
            "oop": 0
        }
    }
    
    # Set state to waiting for start
    await state.set_state(TestStates.waiting_for_start)
    
    # Create keyboard
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать тест", callback_data="start_test")
    
    await message.answer(
        "Добро пожаловать в диагностический тест по Python!\n\n"
        "Тест состоит из 10 вопросов и поможет определить ваши сильные и слабые стороны.\n"
        "На основе результатов мы создадим индивидуальный план обучения.\n\n"
        "Готовы начать?",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "start_test")
async def start_test(callback: CallbackQuery, state: FSMContext):
    """
    Handle the start test button
    """
    await callback.answer()
    
    user_id = callback.from_user.id
    
    # Set state to answering questions
    await state.set_state(TestStates.answering_questions)
    
    # Send the first question
    await send_question(callback.message, user_id)

async def send_question(message: Message, user_id: int):
    """
    Send a question to the user
    """
    # Get user test data
    test_data = user_test_data.get(user_id)
    if not test_data:
        await message.answer("Произошла ошибка. Пожалуйста, начните тест заново с помощью команды /test")
        return
    
    # Get current question
    current_idx = test_data["current_question"]
    if current_idx >= len(test_data["questions"]):
        # No more questions, finish the test
        await finish_test(message, user_id)
        return
    
    question = test_data["questions"][current_idx]
    
    # Create keyboard with options
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(question["options"]):
        builder.button(text=option, callback_data=f"answer_{i}")
    
    # Send question
    await message.answer(
        f"Вопрос {current_idx + 1} из {len(test_data['questions'])}:\n\n"
        f"{question['text']}",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """
    Process the user's answer
    """
    await callback.answer()
    
    user_id = callback.from_user.id
    
    # Get user test data
    test_data = user_test_data.get(user_id)
    if not test_data:
        await callback.message.answer("Произошла ошибка. Пожалуйста, начните тест заново с помощью команды /test")
        return
    
    # Get current question
    current_idx = test_data["current_question"]
    question = test_data["questions"][current_idx]
    
    # Get selected answer
    selected_option = int(callback.data.split("_")[1])
    
    # Store the answer
    test_data["answers"].append({
        "question_id": question["id"],
        "selected_option": selected_option,
        "is_correct": selected_option == question["correct_index"]
    })
    
    # Update category scores
    category = question["category"]
    test_data["category_counts"][category] += 1
    if selected_option == question["correct_index"]:
        test_data["category_scores"][category] += 1
    
    # Move to the next question
    test_data["current_question"] += 1
    
    # Send feedback
    if selected_option == question["correct_index"]:
        await callback.message.answer("✅ Правильно!")
    else:
        correct_option = question["options"][question["correct_index"]]
        await callback.message.answer(f"❌ Неправильно. Правильный ответ: {correct_option}")
    
    # Send the next question
    await send_question(callback.message, user_id)

async def finish_test(message: Message, user_id: int):
    """
    Finish the test and show results
    """
    # Get user test data
    test_data = user_test_data.get(user_id)
    if not test_data:
        await message.answer("Произошла ошибка. Пожалуйста, начните тест заново с помощью команды /test")
        return
    
    # Calculate scores for each category
    category_percentages = {}
    for category in test_data["category_scores"]:
        if test_data["category_counts"][category] > 0:
            score = test_data["category_scores"][category]
            count = test_data["category_counts"][category]
            percentage = (score / count) * 100
            category_percentages[category] = percentage
        else:
            category_percentages[category] = 0
    
    # Find weak areas (categories with score < 60%)
    weak_areas = [category for category, percentage in category_percentages.items() 
                 if percentage < 60 and test_data["category_counts"][category] > 0]
    
    # If no weak areas found, pick the lowest scoring categories
    if not weak_areas and category_percentages:
        sorted_categories = sorted(category_percentages.items(), key=lambda x: x[1])
        weak_areas = [sorted_categories[0][0]]
        if len(sorted_categories) > 1:
            weak_areas.append(sorted_categories[1][0])
    
    # Store test results in database (in a real app)
    # For now, just print them
    
    # Generate learning plan
    learning_plan = generate_learning_plan(weak_areas)
    
    # Format the plan for display
    plan_text = "\n".join([f"День {day}: {topic}" for day, topic in learning_plan.items()])
    
    # Show results
    await message.answer(
        "🎉 Тест завершен! Вот ваши результаты:\n\n"
        + "\n".join([f"{category.capitalize()}: {percentage:.1f}%" for category, percentage in category_percentages.items()])
        + "\n\n"
        + f"Ваши слабые стороны: {', '.join([area.capitalize() for area in weak_areas])}\n\n"
        + "На основе результатов мы создали для вас индивидуальный план обучения:\n\n"
        + plan_text
        + "\n\n"
        + "Готовы начать первый урок? Нажмите /lesson для начала обучения!"
    )
    
    # Clean up test data
    del user_test_data[user_id]