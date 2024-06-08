import json
import os

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'text.json')
with open(file_path, 'r') as file:

# file = open("replics/text.json")
    messages_for_users = json.load(file)

def get_text(text_name: str):
    return messages_for_users[text_name]