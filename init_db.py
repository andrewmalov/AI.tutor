"""
Script to initialize the database with sample data
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

# Load environment variables
load_dotenv()

# Import models
from src.database.models import Base, User, Question, Lesson, Achievement

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Convert SQLite URL to async format if needed
if DATABASE_URL.startswith("sqlite:"):
    DATABASE_URL = DATABASE_URL.replace("sqlite:", "sqlite+aiosqlite:", 1)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Initialize the database, creating all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def populate_db():
    """Populate the database with sample data"""
    async with async_session() as session:
        # Import sample data
        from src.lessons.test_questions import DIAGNOSTIC_TEST
        from src.lessons.lesson_content import LESSONS
        from src.gamification.achievements import ACHIEVEMENTS
        
        # Add test questions
        for question_data in DIAGNOSTIC_TEST:
            question = Question(
                id=question_data["id"],
                is_test_question=True,
                category=question_data["category"],
                text=question_data["text"],
                options=question_data["options"],
                correct_index=question_data["correct_index"]
            )
            session.add(question)
        
        # Add lessons and their questions
        for lesson_data in LESSONS:
            lesson = Lesson(
                id=lesson_data["id"],
                topic=lesson_data["topic"],
                theory=lesson_data["theory"],
                code_example=lesson_data["code_example"]
            )
            session.add(lesson)
            
            # Add lesson questions
            for i, question_data in enumerate(lesson_data["questions"]):
                question = Question(
                    lesson_id=lesson_data["id"],
                    is_test_question=False,
                    category=lesson_data["topic"].split(":")[0].lower(),
                    text=question_data["text"],
                    options=question_data["options"],
                    correct_index=question_data["correct_index"]
                )
                session.add(question)
        
        # Add achievements
        for achievement_data in ACHIEVEMENTS:
            achievement = Achievement(
                id=achievement_data["id"],
                name=achievement_data["name"],
                description=achievement_data["description"],
                xp_reward=achievement_data["xp_reward"]
            )
            session.add(achievement)
        
        # Commit all changes
        await session.commit()

async def main():
    """Main function"""
    await init_db()
    await populate_db()
    print("Database initialized and populated with sample data!")

if __name__ == "__main__":
    asyncio.run(main())