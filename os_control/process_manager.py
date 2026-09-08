import psutil

from os_control.guardrails import (
    is_protected,
    confirm_action
)


def get_top_processes(limit=5):

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):

        try:
            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu": info["cpu_percent"],
                "memory": info["memory_percent"]
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(
        key=lambda x: x["cpu"] or 0,
        reverse=True
    )

    return processes[:limit]


def kill_process(pid):

    try:

        process = psutil.Process(pid)

        name = process.name()

        # 1. Check blacklist FIRST
        if is_protected(name):

            return (
                f"BLOCKED: {name} is a protected process."
            )

        # 2. Ask user before destructive action
        confirmed = confirm_action(
            f"Kill process '{name}' (PID {pid})"
        )

        if not confirmed:
            return "Action cancelled by user."

        # 3. Actually terminate
        process.terminate()

        return (
            f"Process '{name}' "
            f"(PID {pid}) terminated."
        )

    except psutil.NoSuchProcess:

        return f"No process exists with PID {pid}."

    except psutil.AccessDenied:

        return f"Permission denied for PID {pid}."

# if __name__ == "__main__":

#     result = kill_process(95214)

#     print(result)