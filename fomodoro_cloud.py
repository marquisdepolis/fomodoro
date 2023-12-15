import time
import pyscreenshot as ImageGrab
import os
from dotenv import load_dotenv
import replicate
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()  # Hide the main window

# Function to capture the screen
def capture_screen(filename):
    # Capture and save the screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(filename)

# Function to read and parse the to-do list
def read_todo_list(filepath):
    # Read and return tasks from the to-do list
    tasks = []
    with open(filepath, 'r') as file:
        tasks = file.readlines()
    return tasks

# Function to analyze the screenshot with Replicate API
def analyze_screenshot(image_path, replicate_client):
    # Use Replicate API to analyze the image and return the result
    output = replicate_client.run(
        "yorickvp/llava-13b:c293ca6d551ce5e74893ab153c61380f5bcbd80e02d49e08c582de184a8f6c83",
        input={
            "image": open(image_path, "rb"),
            "prompt": "What's going on in this screenshot? Be detailed.",
            "max_tokens": 1024,
            "temperature": 0.2
        }
    )
    return output

def activity_matches_todo_list(analysis_result, todo_list, replicate_client):
    # Format the prompt with analysis result and to-do list
    prompt = """Check if the analyzed content matches any task in the to-do list. Analyzed content: '{analysis_result}'. To-do list: {todo_list}. Give your reply only using the phrase 'NO NOPE IT DOES NOT MATCH' or 'YES YEAH'. There should be no other words in the reply."""

    # Make the LLM call
    output = replicate_client.run(
        "mistralai/mistral-7b-instruct-v0.1:83b6a56e7c828e667f21fd596c338fd4f0039b46bcfa18d973e8e70e455fda70",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 0.9,
            "prompt": prompt,
            "temperature": 0.7,
            "max_new_tokens": 500,
            "min_new_tokens": -1
        }
    )

    # Convert the output to a single string
    response = ' '.join([str(item) for item in output])

    # Check the entire response for the matching phrase
    if "YES" in response:
        return True
    elif "NO" in response:
        return False
    else:
        # Handle unexpected response
        print("Unexpected response from LLM:", response)
        return False

# Function to show a popup if the user is off-track
def show_popup():
    # Use the existing Tkinter root
    messagebox.showinfo("Reminder", "Go back to your to-do list!", parent=root)
    # After displaying the message, ensure the Tkinter window is ready to be used again
    root.update()

# Main function to orchestrate the app
def main():
    # Load environment variables
    load_dotenv()

    # Initialize Replicate client
    replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    while True:
        # Capture the screen every 15 minutes
        capture_screen("screenshot.png")

        # Read the to-do list
        todo_list = read_todo_list("todo.txt")

        # Analyze the screenshot
        analysis_result = analyze_screenshot("screenshot.png", replicate_client)
        print("Debug - Analysis Result:", analysis_result)

        # Check if the current activity matches the to-do list
        if not activity_matches_todo_list(analysis_result, todo_list, replicate_client):
            show_popup()

        # Wait for 15 minutes before the next cycle
        time.sleep(15 * 60)

if __name__ == "__main__":
    main()