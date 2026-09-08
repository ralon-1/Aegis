PROTECTED_PROCESSES = {
    "kernel_task",
    "launchd",
    "WindowServer",
    "loginwindow",
}


def is_protected(process_name):
    return process_name in PROTECTED_PROCESSES


def confirm_action(action):

    answer = input(
        f"\n⚠️ Aegis wants to perform:\n"
        f"{action}\n"
        f"Confirm? (y/n): "
    )

    return answer.lower() == "y"