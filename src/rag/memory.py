class ConversationMemory:

    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

    def format_history(self):

        if not self.history:
            return "No previous conversation."

        formatted = []

        for message in self.history:

            role = message["role"].capitalize()
            content = message["content"]

            formatted.append(
                f"{role}: {content}"
            )

        return "\n".join(formatted)