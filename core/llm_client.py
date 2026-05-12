import os
import time
import requests
import json

class LLMClient:
    """
    Hybrid LLM Adapter for Project JARVIS & FRIDAY.
    Supports:
    - Gemini API (via Google AI SDK or REST)
    - Ollama (Local)
    - Mock (Simulation)
    - Offline Fallback
    """
    def __init__(self, provider=None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "mock")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        
        # Validate Gemini key if provider is set to gemini
        if self.provider == "gemini" and (not self.gemini_api_key or "YOUR_GEMINI" in self.gemini_api_key):
            # print("Warning: Gemini API Key not found. Falling back to Mock mode.")
            self.provider = "mock"

    def chat(self, system_prompt, history, user_input):
        """
        Attempts to get a response from the primary provider.
        Falls back to local/offline if connection fails.
        """
        try:
            if self.provider == "gemini":
                return self._call_gemini(system_prompt, history, user_input)
            elif self.provider == "ollama":
                return self._call_ollama(system_prompt, history, user_input)
            elif self.provider == "mock":
                return self._mock_cloud_response(system_prompt, user_input)
            else:
                return self._offline_fallback(user_input)
        except Exception as e:
            if self.provider != "mock":
                print(f"Provider '{self.provider}' failed ({e}). Falling back to Offline Mode.")
            return self._offline_fallback(user_input)

    def _call_gemini(self, system_prompt, history, user_input):
        # Implementation for Gemini API (REST)
        # Using a simplified REST call for this example
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        headers = {'Content-Type': 'application/json'}
        
        # Combine system prompt with history
        contents = [{"role": "user", "parts": [{"text": system_prompt}]}]
        for item in history[-5:]: # Last 5 context turns
            contents.append({"role": item['role'], "parts": [{"text": item['content']}]})
        contents.append({"role": "user", "parts": [{"text": user_input}]})

        payload = {"contents": contents}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            raise ConnectionError(f"Gemini API Error: {response.text}")

    def _call_ollama(self, system_prompt, history, user_input):
        # Implementation for local Ollama
        payload = {
            "model": "gemma:2b", # Default local model
            "prompt": f"System: {system_prompt}\nUser: {user_input}",
            "stream": False
        }
        response = requests.post(self.ollama_url, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json().get('response')
        else:
            raise ConnectionError("Ollama connection failed.")

    def _mock_cloud_response(self, system_prompt, user_input):
        """Simulates a cloud-based LLM response."""
        time.sleep(0.4)
        if "jarvis" in system_prompt.lower():
            return f"JARVIS (Mock): Sir, I've processed '{user_input}' using the mock cloud adapter."
        return f"FRIDAY (Mock): Boss, request '{user_input}' received. Mock adapter is active."

    def _offline_fallback(self, user_input):
        """Simple rule-based responses when no LLM is available."""
        u = user_input.lower()
        if "time" in u:
            return f"I'm currently offline, but the time is {time.strftime('%H:%M:%S')}."
        return "I'm currently in offline mode and unable to reach my neural core. I've logged your request for when I'm back online."

    def set_provider(self, provider):
        self.provider = provider
