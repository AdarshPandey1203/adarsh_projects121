import json
import os
from datetime import datetime

class Memory:
    def __init__(self, session_id, storage_path='sessions'):
        self.session_id = session_id
        self.storage_path = storage_path
        self.history = []
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        self.load_history()

    def add_message(self, role, content):
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.history.append(message)
        self.save_history()

    def get_history(self):
        return self.history

    def load_history(self):
        session_file = os.path.join(self.storage_path, f"{self.session_id}.json")
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                self.history = json.load(f)

    def save_history(self):
        session_file = os.path.join(self.storage_path, f"{self.session_id}.json")
        with open(session_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def clear_history(self):
        self.history = []
        session_file = os.path.join(self.storage_path, f"{self.session_id}.json")
        if os.path.exists(session_file):
            os.remove(session_file)
