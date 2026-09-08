from ui.overlay import AegisOverlay
from ui.hotkey_listener import HotkeyListener


def main():

    overlay = AegisOverlay()

    # Start hidden
    overlay.hide()

    hotkey = HotkeyListener(
        overlay.toggle
    )

    hotkey.start()

    print("Aegis is running.")
    print("Press Ctrl + Space to toggle Aegis.")

    overlay.run()


if __name__ == "__main__":
    main()