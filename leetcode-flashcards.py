import csv
import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap

# List of Computer Science related emojis
cs_emojis = ["👨‍💻", "👩‍💻", "💻", "🖥️", "⌨️", "🖱️", "🔌", "💾", "💿", "📀", "🕹️", "🖨️", "🖲️", "📱", "🔋", "🔍", "🌐", "📡", "📶", "🛰️", "🔒", "🔓", "🔑", "📊", "📈", "📉", "📁", "📂", "🗂️", "📓", "📔", "🔢", "🧮", "🔬", "🔭", "📡", "🛸", "🤖"]

def create_flashcard(text, filename, is_question=True, emoji=""):
    # Create a new image with a black background
    img = Image.new('RGB', (1080, 1080), color='black')
    d = ImageDraw.Draw(img)

    # Load base fonts with large sizes to adjust down if needed
    try:
        base_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=120)
        emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", size=140)
    except OSError:
        print("Failed to load the specified font. Using default font.")
        base_font = emoji_font = ImageFont.load_default()

    # Set colors
    text_color = (255, 255, 255)  # White
    header_color = (200, 200, 200)  # Light Gray

    # Add a header
    header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=80)
    header = "Question" if is_question else "Answer"
    d.text((60, 60), header, font=header_font, fill=header_color)

    # Add emoji
    emoji_bbox = d.textbbox((0, 0), emoji, font=emoji_font)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    d.text((1080 - emoji_width - 60, 60), emoji, font=emoji_font, fill=header_color)

def create_flashcard(text, filename, is_question=True, emoji=""):
    # Create a new image with a black background
    img = Image.new('RGB', (1080, 1080), color='black')
    d = ImageDraw.Draw(img)

    # Load base fonts with a large initial size
    try:
        base_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=200)
        emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", size=140)
    except OSError:
        print("Failed to load the specified font. Using default font.")
        base_font = emoji_font = ImageFont.load_default()

    # Set colors
    text_color = (255, 255, 255)  # White
    header_color = (200, 200, 200)  # Light Gray

    # Add a header
    header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=80)
    header = "Question" if is_question else "Answer"
    d.text((60, 60), header, font=header_font, fill=header_color)

    # Add emoji
    emoji_bbox = d.textbbox((0, 0), emoji, font=emoji_font)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    d.text((1080 - emoji_width - 60, 60), emoji, font=emoji_font, fill=header_color)

    # Maximum width and height for text area (1000x1000 for visibility)
    max_width = 1000
    max_height = 750  # Reserve space for header and emoji

    # Adjust font size dynamically for main text
    def get_largest_fitting_font(text, font, max_width, max_height):
        size = font.size
        while True:
            wrapped_text = textwrap.wrap(text, width=30)
            total_height = sum(d.textbbox((0, 0), line, font=font)[3] for line in wrapped_text) * 1.2
            if total_height <= max_height and all(d.textbbox((0, 0), line, font=font)[2] <= max_width for line in wrapped_text):
                break
            size -= 2  # Decrease font size slightly
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        return font

    # Get the largest fitting font
    font = get_largest_fitting_font(text, base_font, max_width, max_height)
    wrapped_text = textwrap.wrap(text, width=30)

    # Calculate y-position to center text vertically
    line_height = d.textbbox((0, 0), 'hg', font=font)[3]
    text_height = len(wrapped_text) * line_height * 1.2
    y_text = (1080 - text_height) / 2 + 80  # Adjust for header space

    # Draw each line of text
    for line in wrapped_text:
        line_width = d.textbbox((0, 0), line, font=font)[2]
        x_text = (1080 - line_width) / 2
        d.text((x_text, y_text), line, font=font, fill=text_color)
        y_text += line_height * 1.2

    # Save the image
    img.save(filename)

    # Save the image
    img.save(filename)

def make_filename_friendly(text):
    # Replace spaces with underscores and remove non-alphanumeric characters
    return ''.join(c if c.isalnum() else '_' for c in text).rstrip('_')

def process_csv(csv_file):
    # Create a folder with the same name as the CSV file (without extension)
    folder_name = os.path.splitext(csv_file)[0]
    os.makedirs(folder_name, exist_ok=True)

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['Question']
            answer = row['Answer']
            
            # Select a random emoji for this question-answer pair
            emoji = random.choice(cs_emojis)
            
            # Create filename-friendly version of the question
            friendly_name = make_filename_friendly(question)[:50]  # Limit to 50 characters
            
            question_filename = os.path.join(folder_name, f"{friendly_name}_question.png")
            answer_filename = os.path.join(folder_name, f"{friendly_name}_answer.png")
            
            create_flashcard(question, question_filename, is_question=True, emoji=emoji)
            create_flashcard(answer, answer_filename, is_question=False, emoji=emoji)

    # Move the processed CSV file to the 'complete' folder
    complete_folder = 'complete'
    os.makedirs(complete_folder, exist_ok=True)
    shutil.move(csv_file, os.path.join(complete_folder, os.path.basename(csv_file)))

def process_all_csv_files():
    # Process all CSV files in the current directory
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            print(f"Processing {file}...")
            process_csv(file)
            print(f"Finished processing {file}")

# Usage
process_all_csv_files()
