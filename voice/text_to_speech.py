import subprocess
import threading

class TextToSpeech:
    def __init__(self):
        pass

    def speak(self, text: str):
        if not text:
            return
        
        # Run in a daemon thread so it doesn't block the caller (Tkinter main loop)
        thread = threading.Thread(target=self._speak_sync, args=(text,), daemon=True)
        thread.start()

    def _speak_sync(self, text: str):
        try:
            subprocess.run(["say", text], check=True)
        except Exception as e:
            print(f"TTS Error: {e}")
