import os
from datetime import datetime

class HandoverManager:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir
        self.handover_file = os.path.join(root_dir, 'handover.md')

    def generate_handover(self, current_persona, session_summary):
        """Generates a handover.md file for cross-device development context."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# Project JARVIS & FRIDAY - Development Handover
Generated on: {timestamp}

## 1. Current State
- **Active Persona:** {current_persona['name']}
- **Session End Status:** Success
- **Last Context:** {session_summary}

## 2. Technical Context
- **Phase:** Phase 1 (Base Foundation)
- **Repo Status:** Core modules implemented (Persona, Session, Handover).
- **Environment:** Windows (PowerShell)

## 3. Next Steps (Phase 2 Preview)
- [ ] Implement Voice Interface (TTS/STT).
- [ ] Connect Gemma 3 Flash API/Local.
- [ ] Implement advanced memory/Supabase integration.

## 4. Developer Notes
The system is now modular. To switch personas, use the internal `switch_persona` method in `main.py`.
Chat logs are stored in `data/`.
"""
        with open(self.handover_file, 'w') as f:
            f.write(content)
        print(f"Handover report generated: {self.handover_file}")
