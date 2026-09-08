class ConversationMemory:

    def __init__(self, max_turns=3):
        self.max_turns = max_turns
        self.messages = []

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

        self._trim()

    def add_assistant_message(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

        self._trim()

    def get_messages(self):
        return self.messages

    def _trim(self):

        max_messages = self.max_turns * 2

        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]