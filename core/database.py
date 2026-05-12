import os
import uuid
from datetime import datetime
from supabase import create_client, Client

class SupabaseDatabase:
    """
    Handles real-time synchronization with Supabase.
    Table: chat_logs
    Columns: id, created_at, persona, role, content, session_id
    """
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = None
        
        if self.url and self.key and "YOUR_SUPABASE" not in self.url:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                print(f"Supabase Connection Error: {e}")

    def push_log(self, persona, role, content, session_id):
        """Pushes a single message log to Supabase chat_logs table."""
        if not self.client:
            return False

        try:
            data = {
                "id": str(uuid.uuid4()),
                "created_at": datetime.now().isoformat(),
                "persona": persona,
                "role": role,
                "content": content,
                "session_id": session_id
            }
            # Using synchronous insert
            self.client.table("chat_logs").insert(data).execute()
            return True
        except Exception as e:
            print(f"Supabase Push Error: {e}")
            return False

    def fetch_recent_logs(self, limit=10):
        """Fetches the last N logs to maintain context across devices."""
        if not self.client:
            return []

        try:
            response = self.client.table("chat_logs") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            
            # Convert to history format used by HistoryManager
            logs = response.data
            logs.reverse() # Order by chronological
            return logs
        except Exception as e:
            print(f"Supabase Fetch Error: {e}")
            return []

    def is_active(self):
        return self.client is not None
