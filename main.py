from ai_core import tool_registry
from ai_core.tools import mute_system
from ai_core.llm_client import ask_ai
from ai_core.parser import parse_tool_call,parse_tool_plan
from ai_core.tool_registry import ToolRegistry
from ai_core.memory import ConversationMemory

from ai_core.tools import (
    open_vscode,
    lock_pc,
    get_processes,
    kill_process_tool,
    start_docker,
    mute_system,
    unmute_system,
    set_volume,
    set_brightness
)
from os_control.routines import (
    setup_dev_environment
)

def main():

    registry = ToolRegistry()

    registry.register(
    "setup_dev_environment",
    setup_dev_environment
)
    registry.register(
        "open_vscode",
        open_vscode
    )

    registry.register(
        "set_volume",
        set_volume
    )
    registry.register(
        "set_brightness",
        set_brightness
    )
    registry.register(
        "mute",
        mute_system
    )
    registry.register(
        "unmute",
        unmute_system
    )
    registry.register(
        "lock_pc",
        lock_pc,
        dangerous=True
    )

    registry.register(
        "get_top_processes",
        get_processes
    )

    registry.register(
        "kill_process",
        kill_process_tool,
        dangerous=True
    )

    registry.register(
        "start_docker",
        start_docker
    )

    memory = ConversationMemory(max_turns=3)

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Aegis shutting down...")
            break

        old_history = memory.get_messages().copy()

        response = ask_ai(
            user_input,
            old_history
        )

        memory.add_user_message(user_input)
        memory.add_assistant_message(response)

        print("\nAI ralon testting :")
        print(response)
        

        tool_plan = parse_tool_plan(response)
        print("\nAI ralon tool plan  :")
        print(tool_plan)


        if tool_plan is None:
            continue

        for tool_call in tool_plan.tool_calls:

            print(
                f"\nExecuting: {tool_call.tool_name}"
            )

            if not registry.exists(tool_call.tool_name):

                print(
                    f"Unknown tool: "
                    f"{tool_call.tool_name}"
                )

                continue

            try:

                result = registry.execute(
                    tool_call.tool_name,
                    tool_call.arguments
                )

                print("Result:", result)
                  # ADD THIS: Let the AI know the tool finished successfully
                memory.add_user_message(
                    f"System observation: Tool '{tool_call.tool_name}' executed successfully. Result: {result}"
                )

            except Exception as e:

                print(
                    "Tool execution failed:",
                    e
                )
                 
                # ADD THIS: Let the AI know the tool failed
                memory.add_user_message(
                    f"System observation: Tool '{tool_call.tool_name}' failed with error: {e}"
                )

if __name__ == "__main__":
    main()