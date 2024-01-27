import json
import requests
import time
import pyscreenshot as ImageGrab
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
import base64
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

def generate_text(prompt):
    r = requests.post('http://0.0.0.0:11434/api/generate',
                      json={
                          'model': "mistral",
                          'prompt': prompt,
                      },
                      stream=False)
    full_response = ""    
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_line = json.loads(decoded_line)
            full_response += json_line.get("response", "")
            if json_line.get("done"):
                break

    print(full_response)
    return full_response

def generate_image(prompt, image):
    data = {"model": "llava",
          "prompt": prompt,
          "images": image,
          "stream": False}
    url = "http://0.0.0.0:11434/api/generate"
    response = requests.post(url, data = json.dumps(data))
    response_json = response.json()
    return response_json['response']

def analyze_screenshot(image_path):
    with open(image_path, "rb") as f:
      encoded_string = base64.b64encode(f.read()).decode('utf-8')
    image_array = [encoded_string]
    prompt = "What's going on in this screenshot? Be detailed."
    return generate_image(prompt, image_array)

def activity_matches_todo_list(analysis_result, todo_list):
    prompt = """Check if the analyzed content matches any task in the to-do list. Analyzed content: '{analysis_result}'. To-do list: {todo_list}. Give your reply only using the phrase 'NO NOPE IT DOES NOT MATCH' or 'YES YEAH'. There should be no other words in the reply."""
    print("/n/n we're gonna look at todo list now /n")
    response = generate_text(prompt)

    # Convert the output to a single string
    response = ' '.join([str(item) for item in response])

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
    messagebox.showinfo("Reminder", "Go back to your to-do list!", parent=root)
    root.update()

def main():
    load_dotenv()
    while True:
        capture_screen("screenshot.png")
        todo_list = read_todo_list("todo.txt")
        analysis_result = analyze_screenshot("screenshot.png")
        print("Debug - Analysis Result:", analysis_result)

        if not activity_matches_todo_list(analysis_result, todo_list):
            show_popup()

        # Wait for 15 minutes before the next cycle
        time.sleep(15 * 60)

if __name__ == "__main__":
    main()