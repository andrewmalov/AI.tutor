"""
Module for generating personalized learning plans
"""

# Mapping of topics to lesson IDs
TOPIC_TO_LESSON = {
    "syntax": [1, 3],  # Basic functions, File operations
    "data_types": [3, 7],  # File operations, Iterators and generators
    "functions": [1, 4],  # Basic functions, Decorators
    "loops": [3, 7],  # File operations, Iterators and generators
    "oop": [2, 5]  # Classes and objects, Exception handling
}

# Default lesson order if no weak areas identified
DEFAULT_PLAN = {
    1: "Функции: основы",
    2: "ООП: классы и объекты",
    3: "Работа с файлами",
    4: "Функции: декораторы",
    5: "Обработка исключений",
    6: "Модули и пакеты",
    7: "Итераторы и генераторы"
}

def generate_learning_plan(weak_areas):
    """
    Generate a personalized learning plan based on weak areas
    
    Args:
        weak_areas: List of weak areas (categories)
        
    Returns:
        Dictionary mapping day numbers to lesson topics
    """
    # If no weak areas, return default plan
    if not weak_areas:
        return DEFAULT_PLAN
    
    # Start with an empty plan
    plan = {}
    
    # Add lessons for weak areas first
    day = 1
    for area in weak_areas:
        if area in TOPIC_TO_LESSON:
            for lesson_id in TOPIC_TO_LESSON[area]:
                if day <= 7 and lesson_id not in [plan_lesson for plan_lesson in plan.values()]:
                    plan[day] = DEFAULT_PLAN[lesson_id]
                    day += 1
    
    # Fill remaining days with other lessons
    for lesson_day, topic in DEFAULT_PLAN.items():
        if day <= 7 and topic not in plan.values():
            plan[day] = topic
            day += 1
    
    return plan