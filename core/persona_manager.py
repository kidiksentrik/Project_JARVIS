import json
import os

class PersonaManager:
    def __init__(self, personas_dir='personas'):
        self.personas_dir = personas_dir
        self.personas = {}
        self.current_persona = None
        self.load_all_personas()

    def load_all_personas(self):
        """Loads all JSON files from the personas directory."""
        if not os.path.exists(self.personas_dir):
            print(f"Error: Personas directory '{self.personas_dir}' not found.")
            return

        for filename in os.listdir(self.personas_dir):
            if filename.endswith('.json'):
                path = os.path.join(self.personas_dir, filename)
                with open(path, 'r') as f:
                    persona_data = json.load(f)
                    name = persona_data.get('name', filename[:-5]).upper()
                    self.personas[name] = persona_data
        
        # Default to JARVIS if available
        if 'JARVIS' in self.personas:
            self.current_persona = self.personas['JARVIS']
        elif self.personas:
            self.current_persona = list(self.personas.values())[0]

    def switch_persona(self, name):
        """Switches the active persona by name."""
        name = name.upper()
        if name in self.personas:
            self.current_persona = self.personas[name]
            return True
        return False

    def get_current_persona(self):
        return self.current_persona

    def list_personas(self):
        return list(self.personas.keys())
