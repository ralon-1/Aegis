from os_control.app_control import open_vscode, start_docker


def setup_dev_environment(
    open_vscode_func=open_vscode,
    start_docker_func=start_docker
):

    results = []

    results.append(
        open_vscode_func()
    )

    results.append(
        start_docker_func()
    )

    return {
        "routine": "setup_dev_environment",
        "results": results
    }