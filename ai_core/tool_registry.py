from os_control.guardrails import confirm_action


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(
        self,
        name,
        function,
        dangerous=False,
        description=""
    ):

        self.tools[name] = {
            "function": function,
            "dangerous": dangerous,
            "description": description
        }

    def exists(self, name):
        return name in self.tools

    def execute(self, name, arguments):

        if not self.exists(name):
            raise ValueError(
                f"Unknown tool: {name}"
            )

        tool = self.tools[name]

        function = tool["function"]

        # Safety layer
        if tool["dangerous"]:

            confirmed = confirm_action(
                f"{name} with arguments {arguments}"
            )

            if not confirmed:
                return "Action cancelled by user."

        return function(**arguments)