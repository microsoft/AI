
class MiniAI:
    def __init__(self):
        self.knowledge = {
            "hello": "Hello! I am MiniAI.",
            "ai": "AI stands for Artificial Intelligence.",
            "help": "I can answer simple questions and grow smarter over time.",
            "bye": "Goodbye! See you again."
        }

    def think(self, user_input):
        user_input = user_input.lower()
        for key in self.knowledge:
            if key in user_input:
                return self.knowledge[key]
        return "I am still learning. Can you teach me?"

if __name__ == "__main__":
    ai = MiniAI()
    print("MiniAI is running. Type 'bye' to exit.")

    while True:
        user = input("You: ")
        response = ai.think(user)
        print("MiniAI:", response)
        if "bye" in user.lower():
            break
