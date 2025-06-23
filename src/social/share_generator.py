"""
Module for generating social media shares
"""
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

async def generate_share_image(user_data):
    """
    Generate an image for social media sharing
    
    Args:
        user_data: Dictionary with user data (level, lessons completed, etc.)
        
    Returns:
        BytesIO object with the image
    """
    # In a real implementation, this would create an actual image
    # For MVP, we'll just create a simple image with text
    
    # Create a blank image
    width, height = 1200, 630
    image = Image.new('RGB', (width, height), color=(53, 59, 72))
    
    # Get a drawing context
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fall back to default if not available
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_medium = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw title
    draw.text(
        (width/2, 100),
        "Python Tutor Bot",
        font=font_large,
        fill=(255, 255, 255),
        anchor="mm"
    )
    
    # Draw level
    draw.text(
        (width/2, 250),
        f"Уровень {user_data.get('level', 1)}",
        font=font_large,
        fill=(85, 239, 196),
        anchor="mm"
    )
    
    # Draw lessons completed
    draw.text(
        (width/2, 350),
        f"Пройдено уроков: {len(user_data.get('completed_lessons', []))}",
        font=font_medium,
        fill=(255, 255, 255),
        anchor="mm"
    )
    
    # Draw streak
    draw.text(
        (width/2, 450),
        f"Дней подряд: {user_data.get('streak_days', 0)}",
        font=font_medium,
        fill=(255, 255, 255),
        anchor="mm"
    )
    
    # Draw call to action
    draw.text(
        (width/2, 550),
        "Присоединяйся к обучению!",
        font=font_small,
        fill=(250, 177, 160),
        anchor="mm"
    )
    
    # Save image to BytesIO
    bio = BytesIO()
    image.save(bio, 'PNG')
    bio.seek(0)
    
    return bio