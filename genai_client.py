import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file from the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def _format_history(history):
    formatted_history = []
    for msg in history:
        # The SDK uses 'model' for the assistant role
        role = 'model' if msg['role'] == 'assistant' else msg['role']
        
        # Skip roles the SDK doesn't understand, like our custom 'context' role
        if role not in ('user', 'model'):
            continue

        # Extract the text content
        content = msg.get('content')
        if isinstance(content, dict):
            text = content.get('body', '')
        else:
            text = content

        if not text:
            continue # Skip empty messages

        formatted_history.append({
            'role': role,
            'parts': [{'text': text}]
        })
    return formatted_history

def ask_gemini(prompt, chat_history=None):
    formatted_history = _format_history(chat_history or [])
    chat = model.start_chat(history=formatted_history)
    response = chat.send_message(prompt)
    return response.text
