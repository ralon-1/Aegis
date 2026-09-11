import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
from faster_whisper import WhisperModel


class SpeechToText:
    def __init__(self, model_size="base"):
        self.model_size = model_size
        self.model = None
        self.sample_rate = 16000

    def _load_model(self):
        if self.model is None:
            print("Loading Whisper model...")
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

    def record_and_transcribe(self, duration=5):
        try:
            self._load_model()
        except Exception as e:
            print(f"Failed to load Whisper model: {e}")
            return None

        print("Recording...")
        try:
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()
        except Exception as e:
            print(f"Failed to record audio: {e}")
            return None

        # Write to temporary file for Whisper
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_path = temp_wav.name
        temp_wav.close()

        try:
            with wave.open(temp_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())

            segments, info = self.model.transcribe(temp_path, beam_size=5)
            transcription = "".join([segment.text for segment in segments]).strip()

            return transcription if transcription else None

        except Exception as e:
            print(f"Failed to transcribe: {e}")
            return None
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
