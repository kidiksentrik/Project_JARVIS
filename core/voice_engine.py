# pyrefly: ignore [missing-import]
import pyttsx3
import threading
import queue
import time

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.male_voice_id = None
        self.female_voice_id = None
        self._find_voices()
        
        # Threading/Queue management
        self.speech_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _find_voices(self):
        """Attempts to find male and female voices on the host OS."""
        for voice in self.voices:
            v_name = voice.name.lower()
            if 'male' in v_name or 'david' in v_name or 'mark' in v_name:
                if not self.male_voice_id:
                    self.male_voice_id = voice.id
            elif 'female' in v_name or 'zira' in v_name or 'hazel' in v_name:
                if not self.female_voice_id:
                    self.female_voice_id = voice.id
        
        if not self.male_voice_id and len(self.voices) > 0:
            self.male_voice_id = self.voices[0].id
        if not self.female_voice_id and len(self.voices) > 1:
            self.female_voice_id = self.voices[1].id
        elif not self.female_voice_id:
            self.female_voice_id = self.male_voice_id

    def _worker(self):
        """Worker thread that processes the speech queue sequentially."""
        # Initialize the engine inside the thread to avoid COM context issues
        local_engine = pyttsx3.init()
        while True:
            try:
                # Block until an item is available
                text, gender = self.speech_queue.get()
                
                target_voice = self.male_voice_id if gender == 'male' else self.female_voice_id
                local_engine.setProperty('voice', target_voice)
                local_engine.setProperty('rate', 175)
                
                local_engine.say(text)
                local_engine.runAndWait()
                
                self.speech_queue.task_done()
            except Exception as e:
                print(f"Voice Engine Error: {e}")
                time.sleep(1) # Prevent tight loop on error

    def speak(self, text, gender='male'):
        """Adds text to the speech queue to be processed by the worker thread."""
        if not text:
            return
        self.speech_queue.put((text, gender))

    def list_available_voices(self):
        return [(v.id, v.name) for v in self.voices]
