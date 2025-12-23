from genai_client import ask_gemini

def summarize_text(text, chat_history=None):
    prompt = f"""
Summarize the following content clearly and concisely:

{text}

Format:
TITLE:
SUMMARY:
KEY POINTS:
"""
    return ask_gemini(prompt, chat_history=chat_history)

def summarize_text_short(text, chat_history=None):
    prompt = f"Summarize the following text in one or two sentences: {text}"
    return ask_gemini(prompt, chat_history=chat_history)
