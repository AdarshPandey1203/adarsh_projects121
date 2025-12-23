import json
import traceback
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import re

from search_tool import search_web
from summarizer import summarize_text, summarize_text_short
from document_processor import read_document
from genai_client import ask_gemini
from scraper import scrape_text

from memory import Memory
 
app = Flask(__name__, static_folder='frontend', static_url_path='')

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
 
import re

# ... (existing code)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.form.get("user_input", "").strip()
        chat_id_str = request.form.get("chat_id")
        
        if chat_id_str:
            current_chat_id = int(chat_id_str)
        else:
            current_chat_id = 0
            while os.path.exists(os.path.join('sessions', f"{current_chat_id}.json")):
                current_chat_id += 1
        
        memory = Memory(current_chat_id)
        
        # Handle file uploads
        files = request.files.getlist('file')
        file_content = ''
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                file_content += read_document(file_path) + "\n"
        
        if file_content:
            memory.add_message('context', file_content)
            user_input = f"I have uploaded a file with the following content: {file_content}\n\n{user_input}"

        # URL detection
        url_match = re.match(r'https?://[^\s]+', user_input)
        if url_match:
            url = url_match.group(0)
            scraped_text = scrape_text(url)
            if scraped_text:
                memory.add_message('context', scraped_text)
                assistant_response_content = {
                    'body': f"I have read the content of the URL. You can now ask me questions about it.",
                    'summary': '',
                    'research_papers': []
                }
                memory.add_message('user', user_input)
                memory.add_message('assistant', assistant_response_content)
                return jsonify({
                    'assistant_message': {'content': assistant_response_content},
                    'chat_id': current_chat_id
                })
            else:
                assistant_response_content = {
                    'body': "I'm sorry, I couldn't retrieve the content from that URL.",
                    'summary': '',
                    'research_papers': []
                }
                return jsonify({
                    'assistant_message': {'content': assistant_response_content},
                    'chat_id': current_chat_id
                })

        # If not a URL, proceed with question answering
        conversation_history = memory.get_history()
        context = ""
        for msg in conversation_history:
            if msg['role'] == 'context':
                context += msg['content'] + "\n\n"
        
        if user_input:
            prompt = f"""You are a helpful assistant. Use the following context to answer the user's question. The context may include conversation history and content from web pages the user has provided.

            Context:
            {context}

            Conversation History:
            {[f'{msg["role"]}: {msg["content"]}' for msg in conversation_history if msg['role'] != 'context']}

            User's Current Question:
            {user_input}

            If the context is insufficient to answer the question, perform a web search for relevant information. Answer:
            """
            
            output_text = ask_gemini(prompt, chat_history=conversation_history)
            short_summary = summarize_text_short(output_text, chat_history=conversation_history)

            assistant_response_content = {
                'body': output_text,
                'summary': short_summary,
                'research_papers': []
            }

            memory.add_message('user', user_input)
            memory.add_message('assistant', assistant_response_content)

            return jsonify({
                'assistant_message': {'content': assistant_response_content},
                'chat_id': current_chat_id
            })

    except Exception as e:
        with open("error.log", "a") as f:
            f.write(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'No input provided'}), 400


@app.route("/get_history", methods=["GET"])
def get_history():
    sessions_path = 'sessions'
    history = []
    if os.path.exists(sessions_path):
        for filename in os.listdir(sessions_path):
            if filename.endswith(".json"):
                chat_id = int(filename.split('.')[0])
                with open(os.path.join(sessions_path, filename), 'r') as f:
                    messages = json.load(f)
                    if messages:
                        # Find the first user message to use as a title
                        first_user_message = next((msg['content'] for msg in messages if msg['role'] == 'user'), None)
                        if first_user_message:
                             # Truncate title to 30 characters
                            title = first_user_message[:30] if len(first_user_message) > 30 else first_user_message
                        else:
                            title = "Chat" 
                        history.append({'id': chat_id, 'title': title})
    return jsonify(history)

@app.route("/get_chat/<int:chat_id>", methods=["GET"])
def get_chat(chat_id):
    memory = Memory(chat_id)
    return jsonify(memory.get_history())

@app.route("/delete_chat/<int:chat_id>", methods=["POST"])
def delete_chat(chat_id):
    try:
        session_file = os.path.join('sessions', f"{chat_id}.json")
        if os.path.exists(session_file):
            os.remove(session_file)
            return jsonify({"status": "success"})
        else:
            return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route("/clear_history", methods=["POST"])
def clear_history():
    sessions_path = 'sessions'
    if os.path.exists(sessions_path):
        for filename in os.listdir(sessions_path):
            os.remove(os.path.join(sessions_path, filename))
    return jsonify({"status": "success"})

from research_summarizer import summarize_research

@app.route("/summarize_research", methods=["GET"])
def summarize_research_route():
    try:
        topic = request.args.get("topic")
        if not topic:
            return jsonify({"error": "Topic not provided"}), 400
        
        summary, research_papers = summarize_research(topic)
        
        return jsonify({
            "summary": summary,
            "research_papers": research_papers
        })
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Ensure the uploads directory exists
    upload_folder = os.path.join('uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    app.run(debug=True, port=5001)