import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, 'chat_history.json')
        self.history = []
        self.load_history()

    def load_history(self):
        """Loads history from the JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, ValueError):
                self.history = []

    def add_entry(self, role, content, persona_name):
        """Adds a new chat entry and writes to disk immediately."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "persona": persona_name,
            "content": content
        }
        self.history.append(entry)
        self.save_history() # Immediate persistence

    def save_history(self):
        """Saves the entire history to a JSON file, pretty-printed for git diffs."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def get_context(self, limit=10):
        """Returns the last N messages for LLM context."""
        return self.history[-limit:]

    def clear_history(self):
        self.history = []
        self.save_history()

    def set_context(self, history_data):
        """Overwrites the current history with external data (e.g. from cloud sync)."""
        if isinstance(history_data, list):
            self.history = history_data
            self.save_history()
