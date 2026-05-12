import sys
import os
import time
import keyboard
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.persona_manager import PersonaManager
from core.session_manager import SessionManager
from core.handover_manager import HandoverManager
from core.llm_client import LLMClient
from core.voice_engine import VoiceEngine
from core.history_manager import HistoryManager
from core.database import SupabaseDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# Filler words for thought detection
FILLERS = ["uhm", "hmmm", "well", "...", "err", "actually"]

def detect_thought_pause(text):
    """Detects if the user might be hesitating based on filler words."""
    text = text.strip().lower()
    for filler in FILLERS:
        if text.endswith(filler):
            return True
    return False

def main():
    # Setup directories
    for d in ['data', 'logs', 'personas']:
        if not os.path.exists(d):
            os.makedirs(d)

    # Initialize managers
    persona_mgr = PersonaManager(personas_dir='personas')
    session_mgr = SessionManager(data_dir='data')
    handover_mgr = HandoverManager()
    history_mgr = HistoryManager(data_dir='data')
    llm_client = LLMClient() # Auto-detects provider from .env
    voice_engine = VoiceEngine()
    db = SupabaseDatabase()
    
    # Session ID for cloud tracking
    session_id = str(uuid.uuid4())[:8]

    # Hybrid Sync: Pull latest context from Supabase if active
    if db.is_active():
        cloud_logs = db.fetch_recent_logs(limit=10)
        if cloud_logs:
            # Map Supabase logs to History format
            cloud_history = []
            for log in cloud_logs:
                cloud_history.append({
                    "role": log['role'],
                    "content": log['content'],
                    "persona": log['persona'],
                    "timestamp": log['created_at']
                })
            history_mgr.set_context(cloud_history)
            console.print(f"[italic green]Cloud context synchronized (Session: {session_id}).[/italic green]")

    # Get current persona
    persona = persona_mgr.get_current_persona()
    if not persona:
        console.print("[red]Error: No personas found.[/red]")
        return

    # Calculate time delta for contextual greeting
    time_delta_msg = session_mgr.format_delta_message()
    
    # Header
    console.print(Panel(f"[bold cyan]{persona['name']} ACTIVE[/bold cyan]\n[italic]{persona['description']}[/italic]\n[yellow]{time_delta_msg}[/yellow]", title="Project JARVIS & FRIDAY"))

    # Initial Greeting with Context
    honorific = persona.get('honorific', 'Sir')
    # Inject time-awareness instruction into prompt for the first response
    time_aware_instruction = f"NOTE: It has been {time_delta_msg} since the last session. Mention this naturally in your first greeting."
    
    system_context = f"{persona['system_prompt']} {time_aware_instruction}"
    greeting = llm_client.chat(system_context, history_mgr.get_context(), "Initialize and greet me.")
    
    console.print(f"[bold green]{persona['name']}[/bold green]: {greeting}")
    voice_engine.speak(greeting, gender=persona.get('gender', 'male'))
    
    # Immediate Persistence (Local + Cloud)
    history_mgr.add_entry("assistant", greeting, persona['name'])
    db.push_log(persona['name'], "assistant", greeting, session_id)
    handover_mgr.generate_handover(persona, "Session started with contextual greeting.")

    try:
        while True:
            user_input = Prompt.ask(f"[bold white]You[/bold white]")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            
            # 1. Thought Detection (Filler logic)
            if detect_thought_pause(user_input):
                console.print("[italic yellow](I see you're thinking, Sir. Please continue...)[/italic yellow]")
                # In a real STT scenario, we'd wait. In CLI, we just prompt again or append.
                # For this CLI version, we'll just allow the user to keep typing.
                user_input += " " + Prompt.ask("[bold white](cont.)[/bold white]")

            # 2. 'Hold' Key Logic (Simulation for CLI)
            # Since keyboard.is_pressed can be tricky in some terminal emulators, 
            # we'll check if a modifier key (like 'Alt') was being held.
            if keyboard.is_pressed('alt'):
                console.print("[italic cyan](Holding for your thoughts... Release Alt to proceed)[/italic cyan]")
                while keyboard.is_pressed('alt'):
                    time.sleep(0.1)

            if user_input.lower().startswith('/switch '):
                new_persona_name = user_input.split(' ', 1)[1]
                if persona_mgr.switch_persona(new_persona_name):
                    persona = persona_mgr.get_current_persona()
                    console.print(f"[cyan]Switched to {persona['name']}[/cyan]")
                    switch_msg = f"Systems transferred. I am now online, {persona.get('honorific', 'Boss')}."
                    console.print(f"[bold green]{persona['name']}[/bold green]: {switch_msg}")
                    voice_engine.speak(switch_msg, gender=persona.get('gender', 'male'))
                    continue

            # Log user input (Local + Cloud)
            history_mgr.add_entry("user", user_input, "User")
            db.push_log(persona['name'], "user", user_input, session_id)

            # LLM Call
            system_context = f"{persona['system_prompt']} Current Session Info: {time_delta_msg}"
            response = llm_client.chat(system_context, history_mgr.get_context(), user_input)
            
            # Display and Speak
            console.print(f"[bold green]{persona['name']}[/bold green]: {response}")
            voice_engine.speak(response, gender=persona.get('gender', 'male'))

            # 3. Immediate Persistence after each turn (Local + Cloud)
            history_mgr.add_entry("assistant", response, persona['name'])
            db.push_log(persona['name'], "assistant", response, session_id)
            
            summary = f"Interaction turn: {user_input[:20]}..."
            handover_mgr.generate_handover(persona, summary)

    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted.[/yellow]")
    
    finally:
        session_mgr.save_session()
        console.print("[bold cyan]Data secured. Goodbye, " + persona.get('honorific', 'Sir') + ".[/bold cyan]")
        
        # Git Commit Suggestion
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        console.print(f"\n[bold green]Git Handover Suggestion:[/bold green]")
        console.print(f"git add .")
        console.print(f"git commit -m 'Update handover: {timestamp} (Phase 3 Sync)'")

if __name__ == "__main__":
    main()
