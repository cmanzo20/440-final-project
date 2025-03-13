import os
from gtts import gTTS
import pygame

# Text to be said
mytext = 'Welcome to Wandering in the Woods!'

# Language for text
language = 'en'

# Create obj for saying text
myobj = gTTS(text=mytext, lang=language, slow=False)

# Get current working directory 
current_directory = os.getcwd()
print(current_directory)
# Creates the path for the new mp3 file
save_path = os.path.join(current_directory, "AudioFiles" ,"test.mp3")

# Save converted audio
try:
    myobj.save(save_path)
    print(f"Audio saved to: {save_path}")
except Exception as e:
    print(f"Error saving the file: {e}")

# Initialize the mixer module
pygame.mixer.init()

# Check if the file exists before loading
if os.path.exists(save_path):
    # Load the mp3 file
    pygame.mixer.music.load(save_path)

    # Play the loaded mp3 file
    pygame.mixer.music.play()

    # Wait until the music finishes playing- DO NOT REMOVE THIS CODE or audio may not play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Delay to avoid high CPU usage during the wait
else:
    print(f"File not found: {save_path}")
