from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model to store user information and progress"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Progress tracking
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak_days = Column(Integer, default=0)
    last_lesson_date = Column(DateTime, nullable=True)
    
    # Relationships
    test_results = relationship("TestResult", back_populates="user")
    lesson_progress = relationship("LessonProgress", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class TestResult(Base):
    """Store results of the diagnostic test"""
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_date = Column(DateTime, default=datetime.utcnow)
    
    # Store scores by category
    syntax_score = Column(Float, default=0)
    functions_score = Column(Float, default=0)
    oop_score = Column(Float, default=0)
    data_types_score = Column(Float, default=0)
    loops_score = Column(Float, default=0)
    
    # Store weak areas as a list
    weak_areas = Column(JSON)
    
    # Relationship
    user = relationship("User", back_populates="test_results")
    
    def __repr__(self):
        return f"<TestResult(user_id={self.user_id}, test_date={self.test_date})>"


class Lesson(Base):
    """Lesson content model"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    theory = Column(Text, nullable=False)
    code_example = Column(Text, nullable=True)
    
    # Relationships
    questions = relationship("Question", back_populates="lesson")
    lesson_progress = relationship("LessonProgress", back_populates="lesson")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, topic={self.topic})>"


class Question(Base):
    """Question model for both tests and lessons"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    is_test_question = Column(Boolean, default=False)
    category = Column(String, nullable=False)  # syntax, functions, oop, etc.
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of options
    correct_index = Column(Integer, nullable=False)
    
    # Relationship
    lesson = relationship("Lesson", back_populates="questions")
    
    def __repr__(self):
        return f"<Question(id={self.id}, category={self.category})>"


class LessonProgress(Base):
    """Track user progress through lessons"""
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    xp_earned = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="lesson_progress")
    
    def __repr__(self):
        return f"<LessonProgress(user_id={self.user_id}, lesson_id={self.lesson_id}, completed={self.completed})>"


class Achievement(Base):
    """Achievement definitions"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    xp_reward = Column(Integer, default=0)
    
    # Relationship
    user_achievements = relationship("UserAchievement", back_populates="achievement")
    
    def __repr__(self):
        return f"<Achievement(id={self.id}, name={self.name})>"


class UserAchievement(Base):
    """Track which achievements users have earned"""
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    earned_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class LearningPlan(Base):
    """Store the generated learning plan for each user"""
    __tablename__ = "learning_plans"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    creation_date = Column(DateTime, default=datetime.utcnow)
    plan_data = Column(JSON, nullable=False)  # Store the plan as JSON
    
    def __repr__(self):
        return f"<LearningPlan(user_id={self.user_id}, creation_date={self.creation_date})>"