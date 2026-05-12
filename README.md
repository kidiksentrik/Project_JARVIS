# Project JARVIS & FRIDAY

Personalized AI assistant system with Hybrid Intelligence. Designed for seamless transition between office and home environments.

## 🚀 Current Status: Phase 3 (Supabase & Git Integration)
We have successfully implemented real-time cloud synchronization and multi-provider LLM support.

### Key Features
- **Modular Personas**: Switch between **JARVIS** (Polite/Logical) and **FRIDAY** (Witty/Direct).
- **Hybrid Sync**: Real-time chat history synchronization using **Supabase**.
- **Context Awareness**: Time-delta calculations for natural greetings and session continuity.
- **Queue-based TTS**: Smooth, non-blocking voice engine for high-quality interaction.
- **Smart Development**: Automated `handover.md` generation for cross-device development context.

### Tech Stack
- **Engine**: Gemma 3 Flash (via Ollama or Gemini API)
- **Cloud Database**: Supabase (PostgreSQL)
- **Voice**: pyttsx3 (SAPI5/NSSS)
- **UI**: Rich CLI (Python)
- **Version Control**: Git & GitHub

## 🛠 Project Structure
- `main.py`: Core application loop and integration layer.
- `core/`:
  - `database.py`: Supabase real-time sync handler.
  - `llm_client.py`: Multi-provider adapter.
  - `voice_engine.py`: Queue-based voice output.
  - `persona_manager.py`: AI personality definitions.
  - `session_manager.py`: Time and state tracking.
  - `history_manager.py`: Local JSON persistence.
  - `handover_manager.py`: Dev context generator.

## ⚙️ Configuration
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```env
   LLM_PROVIDER=gemini # or ollama, mock
   GEMINI_API_KEY=your_key
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_anon_key
   ```
3. Run the assistant:
   ```bash
   python main.py
   ```

---
*Created with ❤️ by Antigravity AI*
