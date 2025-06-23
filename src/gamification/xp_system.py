"""
Module for handling XP and levels
"""
from datetime import datetime, timedelta

# Store user XP data in memory (in a real app, this would be in a database)
user_xp_data = {}

# XP thresholds for each level
LEVEL_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5000,
    9: 7500,
    10: 10000
}

async def award_xp(user_id, amount, reason):
    """
    Award XP to a user
    
    Args:
        user_id: User ID
        amount: Amount of XP to award
        reason: Reason for awarding XP
        
    Returns:
        Dictionary with new XP total and level
    """
    # Initialize user data if not exists
    if user_id not in user_xp_data:
        user_xp_data[user_id] = {
            "xp": 0,
            "level": 1,
            "streak_days": 0,
            "last_activity": None,
            "achievements": []
        }
    
    # Update streak
    current_time = datetime.now()
    if user_xp_data[user_id]["last_activity"]:
        last_activity = user_xp_data[user_id]["last_activity"]
        time_diff = current_time - last_activity
        
        # If last activity was between 20-28 hours ago, increment streak
        if timedelta(hours=20) <= time_diff <= timedelta(hours=28):
            user_xp_data[user_id]["streak_days"] += 1
            
            # Check for streak achievements
            if user_xp_data[user_id]["streak_days"] == 3:
                await award_achievement(user_id, "streaker", "Стрикер", "Вы занимались 3 дня подряд!")
        
        # If more than 28 hours, reset streak
        elif time_diff > timedelta(hours=28):
            user_xp_data[user_id]["streak_days"] = 1
    
    # Update last activity
    user_xp_data[user_id]["last_activity"] = current_time
    
    # Add XP
    old_xp = user_xp_data[user_id]["xp"]
    old_level = user_xp_data[user_id]["level"]
    
    user_xp_data[user_id]["xp"] += amount
    
    # Check for level up
    new_level = calculate_level(user_xp_data[user_id]["xp"])
    user_xp_data[user_id]["level"] = new_level
    
    # Return updated data
    return {
        "xp": user_xp_data[user_id]["xp"],
        "level": new_level,
        "level_up": new_level > old_level
    }

def calculate_level(xp):
    """
    Calculate level based on XP
    
    Args:
        xp: XP amount
        
    Returns:
        Level number
    """
    for level, threshold in sorted(LEVEL_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
        if xp >= threshold:
            return level
    return 1

async def get_user_level(user_id):
    """
    Get user's current level
    
    Args:
        user_id: User ID
        
    Returns:
        Level number
    """
    if user_id not in user_xp_data:
        return 1
    
    return user_xp_data[user_id]["level"]

async def award_achievement(user_id, achievement_id, name, description):
    """
    Award an achievement to a user
    
    Args:
        user_id: User ID
        achievement_id: Achievement ID
        name: Achievement name
        description: Achievement description
        
    Returns:
        True if the achievement was newly awarded, False if already had it
    """
    # Initialize user data if not exists
    if user_id not in user_xp_data:
        user_xp_data[user_id] = {
            "xp": 0,
            "level": 1,
            "streak_days": 0,
            "last_activity": None,
            "achievements": []
        }
    
    # Check if user already has this achievement
    for achievement in user_xp_data[user_id]["achievements"]:
        if achievement["id"] == achievement_id:
            return False
    
    # Award the achievement
    user_xp_data[user_id]["achievements"].append({
        "id": achievement_id,
        "name": name,
        "description": description,
        "earned_date": datetime.now()
    })
    
    # Award XP for the achievement (50 XP per achievement)
    await award_xp(user_id, 50, f"Достижение: {name}")
    
    return True