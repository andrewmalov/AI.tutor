"""
Module for handling achievements
"""

# List of available achievements
ACHIEVEMENTS = [
    {
        "id": "beginner",
        "name": "Новичок",
        "description": "Пройдите свой первый урок",
        "xp_reward": 50
    },
    {
        "id": "streaker",
        "name": "Стрикер",
        "description": "Занимайтесь 3 дня подряд",
        "xp_reward": 100
    },
    {
        "id": "functions_guru",
        "name": "Гуру функций",
        "description": "Получите 80% правильных ответов по теме 'Функции'",
        "xp_reward": 150
    },
    {
        "id": "oop_master",
        "name": "Мастер ООП",
        "description": "Получите 80% правильных ответов по теме 'ООП'",
        "xp_reward": 150
    },
    {
        "id": "halfway",
        "name": "На полпути",
        "description": "Пройдите 4 урока",
        "xp_reward": 200
    },
    {
        "id": "graduate",
        "name": "Выпускник",
        "description": "Пройдите все 7 уроков",
        "xp_reward": 500
    },
    {
        "id": "perfect_score",
        "name": "Идеальный результат",
        "description": "Получите 100% за урок",
        "xp_reward": 100
    },
    {
        "id": "social_butterfly",
        "name": "Социальная бабочка",
        "description": "Поделитесь своим прогрессом 3 раза",
        "xp_reward": 150
    }
]

def get_achievement_by_id(achievement_id):
    """
    Get achievement by ID
    
    Args:
        achievement_id: ID of the achievement to retrieve
        
    Returns:
        Achievement dictionary or None if not found
    """
    for achievement in ACHIEVEMENTS:
        if achievement["id"] == achievement_id:
            return achievement
    return None