import json

file = open("replics/text.json")
messages_for_users = json.load(file)

def get_text(text_name: str):
    return messages_for_users[text_name]