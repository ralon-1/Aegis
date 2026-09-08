from pynput import keyboard


class HotkeyListener:
    def __init__(self, callback):
        self.callback = callback

        self.listener = keyboard.GlobalHotKeys({
            "<ctrl>+<space>": self.handle_hotkey
        })

    def handle_hotkey(self):
        self.callback()

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
    
    
if __name__ == "__main__":

    def test():
        print("🔥 Aegis hotkey detected!")

    listener = HotkeyListener(test)

    print("Press Ctrl + Space...")
    listener.start()

    listener.listener.join()