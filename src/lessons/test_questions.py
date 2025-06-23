"""
Module containing diagnostic test questions
"""

# Initial set of diagnostic test questions
DIAGNOSTIC_TEST = [
    {
        "id": 1,
        "category": "syntax",
        "text": "Какой символ используется для комментариев в Python?",
        "options": ["//", "#", "/*", "<!--"],
        "correct_index": 1
    },
    {
        "id": 2,
        "category": "data_types",
        "text": "Какой из перечисленных типов данных является изменяемым (mutable)?",
        "options": ["int", "str", "tuple", "list"],
        "correct_index": 3
    },
    {
        "id": 3,
        "category": "functions",
        "text": "Как объявить функцию в Python?",
        "options": ["function my_func():", "def my_func():", "func my_func():", "my_func():"],
        "correct_index": 1
    },
    {
        "id": 4,
        "category": "loops",
        "text": "Какой цикл используется для итерации по элементам списка?",
        "options": ["for", "while", "do-while", "foreach"],
        "correct_index": 0
    },
    {
        "id": 5,
        "category": "oop",
        "text": "Как создать класс в Python?",
        "options": ["class MyClass {}", "class MyClass():", "class MyClass:", "create class MyClass:"],
        "correct_index": 2
    },
    {
        "id": 6,
        "category": "syntax",
        "text": "Какой оператор используется для проверки равенства в Python?",
        "options": ["=", "==", "===", "equals"],
        "correct_index": 1
    },
    {
        "id": 7,
        "category": "functions",
        "text": "Что такое *args в функции Python?",
        "options": [
            "Обязательный аргумент", 
            "Переменное количество позиционных аргументов", 
            "Переменное количество именованных аргументов", 
            "Аргумент со значением по умолчанию"
        ],
        "correct_index": 1
    },
    {
        "id": 8,
        "category": "data_types",
        "text": "Какой метод используется для добавления элемента в список?",
        "options": ["add()", "append()", "insert()", "push()"],
        "correct_index": 1
    },
    {
        "id": 9,
        "category": "oop",
        "text": "Что такое self в методах класса Python?",
        "options": [
            "Ключевое слово для создания приватных методов", 
            "Ссылка на экземпляр класса", 
            "Ссылка на родительский класс", 
            "Обязательное имя первого метода в классе"
        ],
        "correct_index": 1
    },
    {
        "id": 10,
        "category": "loops",
        "text": "Какое ключевое слово используется для прерывания цикла?",
        "options": ["exit", "break", "stop", "continue"],
        "correct_index": 1
    },
    {
        "id": 11,
        "category": "functions",
        "text": "Что такое лямбда-функция в Python?",
        "options": [
            "Функция с множеством аргументов", 
            "Анонимная функция", 
            "Функция, которая всегда возвращает True", 
            "Функция внутри класса"
        ],
        "correct_index": 1
    },
    {
        "id": 12,
        "category": "data_types",
        "text": "Какой тип данных используется для хранения уникальных элементов?",
        "options": ["list", "tuple", "set", "dict"],
        "correct_index": 2
    },
    {
        "id": 13,
        "category": "oop",
        "text": "Что такое наследование в ООП?",
        "options": [
            "Создание нескольких экземпляров класса", 
            "Возможность класса иметь несколько методов", 
            "Возможность класса наследовать атрибуты и методы другого класса", 
            "Скрытие данных от внешнего доступа"
        ],
        "correct_index": 2
    },
    {
        "id": 14,
        "category": "syntax",
        "text": "Как создать многострочный комментарий в Python?",
        "options": [
            "// Комментарий //", 
            "/* Комментарий */", 
            "''' Комментарий '''", 
            "<!-- Комментарий -->"
        ],
        "correct_index": 2
    },
    {
        "id": 15,
        "category": "loops",
        "text": "Что делает оператор continue в цикле?",
        "options": [
            "Завершает цикл", 
            "Пропускает текущую итерацию и переходит к следующей", 
            "Приостанавливает выполнение цикла", 
            "Возвращает значение из цикла"
        ],
        "correct_index": 1
    }
]

def get_test_questions(count=10):
    """
    Get a subset of test questions
    
    Args:
        count: Number of questions to return
        
    Returns:
        List of question dictionaries
    """
    import random
    # Ensure we don't request more questions than available
    count = min(count, len(DIAGNOSTIC_TEST))
    # Return a random selection of questions
    return random.sample(DIAGNOSTIC_TEST, count)