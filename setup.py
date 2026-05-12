import os
import time
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def jarvis_print(text, style="bold green"):
    console.print(f"[bold cyan]SYSTEM:[/bold cyan] {text}", style=style)
    time.sleep(0.5)

def run_setup():
    clear_screen()
    console.print(Panel.fit(
        "[bold cyan]PROJECT JARVIS & FRIDAY - SYSTEMS INITIALIZATION[/bold cyan]",
        subtitle="Vibe Coding Edition",
        border_style="cyan"
    ))
    
    jarvis_print("Initializing environment onboarding protocols...")
    
    # 1. Install Dependencies
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Installing required dependencies...", total=None)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            jarvis_print("Dependencies verified and installed.", style="green")
        except Exception as e:
            console.print(f"[red]Error installing dependencies: {e}[/red]")
            return

    # 2. Check for .env
    if os.path.exists(".env"):
        overwrite = Confirm.ask("[yellow]An existing .env file was detected. Do you wish to override the current configurations?[/yellow]")
        if not overwrite:
            jarvis_print("Maintaining current system integrity. Setup aborted.")
            return

    # 3. Interactive Configuration
    console.print("\n[bold yellow]--- CORE CONFIGURATION ---[/bold yellow]")
    
    provider = Prompt.ask("[cyan]Choose LLM Provider[/cyan]", choices=["ollama", "gemini", "mock"], default="ollama")
    
    gemini_key = "YOUR_GEMINI_API_KEY_HERE"
    ollama_url = "http://localhost:11434/api/generate"

    if provider == "ollama":
        jarvis_print("Local AI Mode selected (Ollama/Gemma).")
        ollama_url = Prompt.ask("[cyan]Enter Ollama Endpoint[/cyan]", default="http://localhost:11434/api/generate")
        console.print("[italic white]Note: Ensure 'ollama run gemma' is active on your machine.[/italic white]")
    elif provider == "gemini":
        jarvis_print("Cloud AI Mode selected (Gemini API).")
        console.print("  - Get Key: [link=https://aistudio.google.com/app/apikey]https://aistudio.google.com/app/apikey[/link]")
        gemini_key = Prompt.ask("[cyan]Enter Gemini API Key[/cyan]", password=True)

    console.print("\n[bold yellow]--- CLOUD SYNC CONFIGURATION ---[/bold yellow]")
    console.print("  - Supabase Project: [link=https://supabase.com/dashboard/project/_/settings/api]https://supabase.com/dashboard/project/_/settings/api[/link]")
    supabase_url = Prompt.ask("[cyan]Enter Supabase URL[/cyan]", default="https://yjqwxtunbejfksyxijrs.supabase.co")
    supabase_key = Prompt.ask("[cyan]Enter Supabase Anon Key[/cyan]", password=True)

    # 4. Generate .env
    jarvis_print("Generating encrypted configuration layer (.env)...")
    env_content = f"""# Project JARVIS & FRIDAY - Environment Configuration

# LLM Configuration
LLM_PROVIDER={provider}
GEMINI_API_KEY={gemini_key}
OLLAMA_URL={ollama_url}

# Supabase Hybrid Sync Configuration
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}

# Voice Configuration
VOICE_RATE=175
"""
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    jarvis_print("Configuration secured.")

    # 5. Final Touch
    console.print("\n" + Panel(
        "[bold green]SYSTEMS ONLINE.[/bold green]\n\n"
        "You can now run the assistant using: [bold yellow]python main.py[/bold yellow]\n"
        "Welcome back, Sir.",
        title="Onboarding Complete",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        console.print("\n[red]Initialization sequence interrupted by user.[/red]")
        sys.exit(0)
