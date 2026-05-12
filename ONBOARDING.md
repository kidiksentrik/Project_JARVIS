# ⚡ Quick Onboarding Guide (New Device)

Follow these steps to bring JARVIS/FRIDAY online on a new machine.

## 1. Prerequisites
- Python 3.10+ installed.
- Git installed.
- **Ollama** installed (for Local AI mode).
- Run: `ollama pull gemma` (or your preferred local model).

## 2. Bootstrapping
```bash
# Clone the repository
git clone https://github.com/kidiksentrik/Project_JARVIS.git
cd Project_JARVIS

# Run the interactive setup
python setup.py
```

## 3. Configuration Access
During setup, you will need:
- **Local AI (Ollama)**: No key required, just ensure Ollama is running.
- **Cloud AI (Gemini)**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Cloud Sync (Supabase)**: [Supabase Project Settings](https://supabase.com/dashboard/project/_/settings/api)

## 4. Run Assistant
```bash
python main.py
```

---
*Status: Ready for Deployment.*
