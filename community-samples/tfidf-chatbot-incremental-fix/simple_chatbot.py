from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack
import numpy as np
import readline


class SimpleChatBot:
    def __init__(self, pairs=None, rebuild_every=20):
        """
        pairs: list of (user_text, bot_answer) tuples.
        rebuild_every: how many learn_from_pair calls to allow before doing a
            full TF-IDF refit, to resync vocabulary/IDF weights.
        """
        self.pairs = pairs or []
        self.rebuild_every = rebuild_every
        self._pending_since_rebuild = 0
        self._build_vectorizer()

    def _build_vectorizer(self):
        self.user_texts = [p[0] for p in self.pairs]
        if self.user_texts:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
            self.user_tfidf = self.vectorizer.fit_transform(self.user_texts)
        else:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
            self.user_tfidf = None
        self._pending_since_rebuild = 0

    def respond(self, text, top_k=1):
        text = text.strip()
        if not text:
            return "Say something."

        if not self.user_texts:
            return "I have no examples yet. Teach me with: learn: your text => my answer"

        x = self.vectorizer.transform([text])
        sims = cosine_similarity(x, self.user_tfidf).flatten()
        best_idx = np.argmax(sims)
        best_score = sims[best_idx]

        if best_score < 0.25:
            return ("That's interesting but I don't have a good response for it. "
                    "Teach me with: learn: question => answer")

        if top_k > 1:
            top_indices = np.argsort(sims)[-top_k:]
            chosen = np.random.choice(top_indices)
            return self.pairs[chosen][1]
        return self.pairs[best_idx][1]

    def learn_from_pair(self, user_text, bot_answer):
        """Add a new example without refitting TF-IDF on every call."""
        user_text, bot_answer = user_text.strip(), bot_answer.strip()
        self.pairs.append((user_text, bot_answer))
        self.user_texts.append(user_text)

        if self.user_tfidf is None:
            self._build_vectorizer()  # first example needs a real fit
            return

        # Reuse the already-fitted vocabulary/IDF weights instead of refitting.
        new_vec = self.vectorizer.transform([user_text])
        self.user_tfidf = vstack([self.user_tfidf, new_vec])
        self._pending_since_rebuild += 1

        # transform() drops n-grams outside the last-fitted vocabulary, so
        # periodically do a full rebuild to pick up new terms/IDF weights.
        if self._pending_since_rebuild >= self.rebuild_every:
            self._build_vectorizer()

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for u, b in self.pairs:
                u_escaped = u.replace("\t", "    ").replace("\n", " ")
                b_escaped = b.replace("\t", "    ").replace("\n", " ")
                f.write(u_escaped + "\t" + b_escaped + "\n")

    def load_from_file(self, path):
        new_pairs = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) >= 2:
                        new_pairs.append((parts[0], "\t".join(parts[1:])))
            self.pairs = new_pairs
            self._build_vectorizer()
        except FileNotFoundError:
            print(f"No dataset found at {path}; starting with an empty dataset.")


def demo():
    initial_pairs = [
        ("hello", "Greetings. What do you wish to know?"),
        ("how are you", "Adequate. And you?"),
        ("what is chess", "Chess is a strategic board game where anticipation is essential."),
        ("teach me chess", "Start with the basics: develop pieces, control the center, avoid early king weaknesses."),
        ("tell a joke", "Two rooks walk onto the board... the rest is legend."),
        ("thanks", "You're welcome. My circuits shine with satisfaction."),
    ]

    bot = SimpleChatBot(initial_pairs)
    bot.load_from_file("my_bot_memory.txt")

    print("Simple ChatBot (TF-IDF retrieval). Type 'quit' to stop.")
    print("Teach the bot new behavior with: learn: your question => my answer")
    print("Save memory with: save")
    print("Load memory with: load")
    print("-" * 60)

    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEnding. Memory is being saved automatically.")
            bot.save_to_file("my_bot_memory.txt")
            break

        if not user:
            continue

        if user.lower() in ("quit", "exit", "stop"):
            print("Bot: Goodbye.")
            bot.save_to_file("my_bot_memory.txt")
            break

        if user.lower().startswith("learn:"):
            payload = user[6:].strip()
            if "=>" in payload:
                q, a = payload.split("=>", 1)
                bot.learn_from_pair(q.strip(), a.strip())
                print("Bot: Acknowledged. I've stored that.")
            else:
                print("Bot: Invalid learn format. Use: learn: question => answer")
            continue

        if user.lower() == "save":
            bot.save_to_file("my_bot_memory.txt")
            print("Bot: memory saved to my_bot_memory.txt")
            continue

        if user.lower() == "load":
            bot.load_from_file("my_bot_memory.txt")
            print("Bot: memory loaded (my_bot_memory.txt)")
            continue

        reply = bot.respond(user, top_k=3)
        print("Bot:", reply)


if __name__ == "__main__":
    demo()
