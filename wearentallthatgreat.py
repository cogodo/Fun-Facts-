import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
from datetime import datetime, timedelta
import webbrowser
import os


fact_number = random.randint(1,27)

df = pd.read_csv('facts.csv')


fotd = df.iloc[fact_number]

text = f"Fact of the Day: \n Title: {fotd['Title']} \n Timeframe: {fotd['Timeframe']} \n Agency: {fotd['Agency']} \n Summary: {fotd['Summary']}"

width, height = 800, 600
background_color = (200,200,200)
font_color = (0,0,255)
font_path = "~/ComicSansMS.ttf"  # Ensure you have this font or specify a full path to a font file
font_size = 10


def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a given width when being drawn on an image.
    """
    lines = []
    # If the text width is smaller than the image width, then no need to wrap
    if font.getsize(text)[0]  <= max_width:
        return [text]
    # Split the text into words
    words = text.split(' ')
    i = 0
    # While there are words left to be checked
    while i < len(words):
        line = ''
        # Keep adding words to the line until it exceeds the width
        while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
            line += words[i] + " "
            i += 1
        if not line:
            # If the line is empty, force-include the next word (to avoid an infinite loop with very long words)
            line = words[i]
            i += 1
        # Remove trailing space
        line = line.rstrip()
        lines.append(line)
    return lines

def create_image_with_text(text, width, height, bg_color, font_color, font_path, font_size):
    image = Image.open('cat-war.gif')
    image = image.convert('RGB')
    image = image.filter(ImageFilter.BLUR)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(image)
    width = image.width
    height = image.height
    # Wrap the text
    lines = wrap_text(text, font, width - 20)  # Assuming a margin of 10 pixels on each side

    # Calculate the height of the text block
    text_height = sum(font.getsize(line)[1] for line in lines)
    
    # Calculate initial Y position to vertically center the text block
    y = (height - text_height) / 5

    # Draw each line of text
    for line in lines:
        text_width, line_height = draw.textsize(line, font=font)
        x = (width - text_width) / 2  # Center each line
        draw.text((x, y), line, font=font, fill=font_color)
        y += line_height  # Move to the next line

    return image

def calculate_sleep_duration(hour=10, minute=0):
    now = datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_run < now:
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()

while True:
    the_funny = create_image_with_text(text, width, height, background_color, font_color, font_path, font_size)
    gif_path = "fact_of_the_day.gif"
    the_funny.save(gif_path, save_all=True, duration=500, loop=0)
    webbrowser.open('file://' + os.path.realpath(gif_path))
    sleep_duration = calculate_sleep_duration()  
    print(f"Sleeping for {sleep_duration} seconds.")
    time.sleep(sleep_duration)
    # I would add animation in some capacity if I knew where to start
    # Found a neat github repo but it seemed way too complicated for this
    
