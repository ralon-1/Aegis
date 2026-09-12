PROTECTED_PROCESSES = {
    "kernel_task",
    "launchd",
    "WindowServer",
    "loginwindow",
}


def is_protected(process_name):
    return process_name in PROTECTED_PROCESSES


def _default_confirm_action(action):
    answer = input(
        f"\n⚠️ Aegis wants to perform:\n"
        f"{action}\n"
        f"Confirm? (y/n): "
    )
    return answer.lower() == "y"

CONFIRMATION_HANDLER = _default_confirm_action

def set_confirmation_handler(handler):
    global CONFIRMATION_HANDLER
    CONFIRMATION_HANDLER = handler

def confirm_action(action):
    return CONFIRMATION_HANDLER(action)