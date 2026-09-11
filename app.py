from ai_core.llm_client import ask_ai
from ai_core.parser import parse_tool_plan
from ai_core.memory import ConversationMemory
from ai_core.tool_registry import ToolRegistry
from ai_core.tools import *

import threading
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech

from ui.overlay import AegisOverlay
from ui.hotkey_listener import HotkeyListener


class AegisApp:

    def __init__(self):

        self.memory = ConversationMemory(max_turns=3)

        self.registry = ToolRegistry()

        self.register_tools()

        self.stt = SpeechToText()
        self.tts = TextToSpeech()

        self.overlay = AegisOverlay(
            self.handle_command,
            self.start_voice_command_thread
        )

        self.overlay.hide()

        self.hotkey = HotkeyListener(
            self.overlay.toggle
        )

        self.hotkey.start()

    def register_tools(self):

        self.registry.register(
            "open_vscode",
            open_vscode
        )

        self.registry.register(
            "start_docker",
            start_docker
        )

        self.registry.register(
            "setup_dev_environment",
            setup_dev_environment
        )

        self.registry.register(
            "set_volume",
            set_volume
        )

        self.registry.register(
            "mute",
            mute
        )

        self.registry.register(
            "unmute",
            unmute
        )

        self.registry.register(
            "set_brightness",
            set_brightness
        )

        self.registry.register(
            "lock_pc",
            lock_pc,
            dangerous=True
        )

        self.registry.register(
            "get_top_processes",
            get_processes
        )

        self.registry.register(
            "kill_process",
            kill_process_tool,
            dangerous=True
        )

    def start_voice_command_thread(self):
        threading.Thread(target=self.handle_voice_command, daemon=True).start()

    def handle_voice_command(self):
        self.overlay.set_status("🎤 Listening...")
        
        text = self.stt.record_and_transcribe(duration=5)
        
        if not text:
            self.overlay.set_status("Could not understand.")
            self.tts.speak("I couldn't understand that.")
            self.overlay.root.after(3000, lambda: self.overlay.set_status(""))
            return
            
        self.overlay.set_status("Processing...")
        
        self.handle_command(text, speak=True)
        
        self.overlay.set_status("")

    def handle_command(self, command, speak=False):

        print("\nUser:", command)

        history = self.memory.get_messages().copy()

        response = ask_ai(
            command,
            history
        )

        print("AI:", response)

        self.memory.add_user_message(command)
        self.memory.add_assistant_message(response)

        tool_plan = parse_tool_plan(response)

        if tool_plan is None:
            if speak:
                self.tts.speak("Sorry, I could not understand the AI response.")
            print("Aegis could not understand the AI response.")
            return

        if speak and tool_plan.response:
            self.overlay.set_status("🔊 Speaking...")
            self.tts.speak(tool_plan.response)
            self.overlay.root.after(2000, lambda: self.overlay.set_status(""))

        for tool_call in tool_plan.tool_calls:

            tool_name = tool_call.tool_name
            arguments = tool_call.arguments

            print(
                f"Executing: {tool_name} {arguments}"
            )

            if not self.registry.exists(tool_name):

                print(
                    f"Unknown tool: {tool_name}"
                )

                continue

            try:

                result = self.registry.execute(
                    tool_name,
                    arguments
                )

                print("Result:", result)

            except Exception as e:

                print(
                    f"Tool execution failed: {e}"
                )

    def run(self):

        print("Aegis is running.")
        print("Press Ctrl + Space to open Aegis.")

        self.overlay.run()


if __name__ == "__main__":

    app = AegisApp()
    app.run()