from os_control.process_manager import (
    get_top_processes,
    kill_process
)
from os_control.app_control import (
    open_vscode,
    start_docker
)
from os_control.hardware_control import (
    set_volume as hw_set_volume,
    mute,
    unmute,
    set_brightness as hw_set_brightness,
    lock_screen
)
from os_control.routines import setup_dev_environment


import subprocess



def set_volume(level):
    return hw_set_volume(level)

def set_brightness(level):
    return hw_set_brightness(level)

def mute_system():
    return mute()


def unmute_system():
    return unmute()


def lock_pc():
    return lock_screen()



def get_processes():
    return get_top_processes()

def kill_process_tool(pid):
    return kill_process(pid)


# if __name__ == "__main__":
#     print(open_vscode())