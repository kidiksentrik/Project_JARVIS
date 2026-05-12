import json
import os
from datetime import datetime

class SessionManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.session_file = os.path.join(data_dir, 'session.json')
        self.last_interaction = None
        self.current_session_start = datetime.now()
        self.load_session()

    def load_session(self):
        """Loads the last session data from disk."""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    last_time_str = data.get('last_interaction')
                    if last_time_str:
                        self.last_interaction = datetime.fromisoformat(last_time_str)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Could not load session file: {e}")

    def save_session(self):
        """Saves current session metadata to disk."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        data = {
            'last_interaction': datetime.now().isoformat(),
            'session_start': self.current_session_start.isoformat()
        }
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_time_delta(self):
        """Calculates the time difference since the last interaction."""
        if not self.last_interaction:
            return None
        
        delta = datetime.now() - self.last_interaction
        
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return {
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_seconds': delta.total_seconds()
        }

    def format_delta_message(self):
        """Returns a human-readable string of the time delta."""
        delta = self.get_time_delta()
        if not delta:
            return "This is our first interaction in this environment."
        
        parts = []
        if delta['hours'] > 0:
            parts.append(f"{delta['hours']} hours")
        if delta['minutes'] > 0:
            parts.append(f"{delta['minutes']} minutes")
        
        if not parts:
            return f"Welcome back. It has been less than a minute since your last interaction."
        
        return f"Welcome back. It has been {' and '.join(parts)} since we last spoke."
