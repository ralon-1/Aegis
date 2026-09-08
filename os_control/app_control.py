import subprocess


def open_vscode():

    try:

        subprocess.Popen(
            ["open", "-a", "Visual Studio Code"]
        )

        return "VS Code opened successfully."

    except Exception as e:

        return f"Failed to open VS Code: {e}"


def start_docker():

    try:

        subprocess.Popen(
            ["open", "-a", "Docker"]
        )

        return "Docker Desktop started."

    except Exception as e:

        return f"Failed to start Docker: {e}"