from glm import call_gpt

QUESTION_PREFIX = "Q:"
GUESS_PREFIX = "GUESS:"


def _reply_content(response):
    return response["content"].strip()


class GuesserAgent:
    '''Agent that guesses the secret animal by asking yes/no questions.'''

    def __init__(self, max_questions=20):
        self.max_questions = max_questions
        self.questions_asked = 0
        self.messages = [{
            "role": "user",
            "content": (
                "Play 20 questions. I am thinking of a type of animal. "
                "Guess which animal it is by asking yes or no questions and using "
                "the answers to narrow down the possibilities. "
                f"You may ask at most {max_questions} questions in total. "
                "Every single reply from you must start with exactly one of these two prefixes:\n"
                f"{QUESTION_PREFIX} <one yes or no question> - never include an animal name in the question\n"
                f"{GUESS_PREFIX} <animal name> - only when you are confident you know the answer\n"
                "Take y to mean yes and n to mean no. "
                "Now ask your first question."
            ),
        }]

    def next_move(self, feedback=None):
        '''Returns (kind, text) where kind is "question" or "guess".'''
        if feedback:
            self.messages.append({"role": "user", "content": feedback})
        if self.questions_asked >= self.max_questions:
            self.messages.append({
                "role": "user",
                "content": "You have no questions left. You must reply with "
                           f"{GUESS_PREFIX} <animal name> now.",
            })
        reply = _reply_content(call_gpt(None, self.messages))
        self.messages.append({"role": "assistant", "content": reply})
        kind, text = self._parse(reply)
        if kind == "question":
            self.questions_asked += 1
        return kind, text

    @staticmethod
    def _parse(reply):
        if reply.startswith(GUESS_PREFIX):
            return "guess", reply[len(GUESS_PREFIX):].strip()
        if reply.startswith(QUESTION_PREFIX):
            return "question", reply[len(QUESTION_PREFIX):].strip()
        # Fallback when the model ignores the prefix format
        if "?" in reply:
            return "question", reply
        return "guess", reply


class AnswererAgent:
    '''Agent that knows the secret animal and answers yes/no questions about it.'''

    def __init__(self, animal):
        self.animal = animal
        self.messages = [{
            "role": "user",
            "content": (
                f"You are playing 20 questions. The secret animal is: {animal}. "
                "The other player will ask you yes or no questions about it. "
                "Answer every question with exactly one word, Yes or No. "
                "No explanations and no extra words."
            ),
        }]

    def answer(self, question):
        self.messages.append({"role": "user", "content": f"Question: {question}"})
        reply = _reply_content(call_gpt(None, self.messages))
        self.messages.append({"role": "assistant", "content": reply})
        return reply