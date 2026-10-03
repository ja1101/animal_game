from animal import get_random_animal
from glm import call_gpt
from re import sub

def normalized(text):
    return sub(r"\W+", " ", text.lower()).strip()

def main():
    conv = []
    animal = get_random_animal()
    print(animal)
    p1 = "Play 20 questions. " + \
    "I am thinking of a type of animal. Your task will be to guess which type it is " + \
    "by asking yes or no questions and keep track of all answers to narrow down the possibilities. " + \
    "Never include an animal name in your questions - " + \
    "they must be answerable with yes or no. Take y to mean yes and n to mean no." + \
    "If you are confident you know the answer, respond with just the animal name by itself. " + \
    "So, ask your first question."
    gpt_resp = call_gpt(p1)
    conv.append(p1)
    resp = gpt_resp["content"]
    print(resp)
    conv.append(resp)
    while True:
        if animal in normalized(resp):
            print("Correct guess from AI!")
            #return
        q = input("Respond yes or no to AI: ").lower()
        conv.append(q)
        if "give up" in q:
            print("The animal was: " + animal)
            return
        gpt_resp = call_gpt(f"The answer to your question is {q}. " + 
        f"Conversation so far: {" ".join(conv)}. " +
        "Now ask your next question based on the information you have so far.")
        resp = gpt_resp["content"]
        print(resp)
        conv.append(resp)

if __name__ == "__main__":
    #print(call_gpt("Which model are you?")["content"])
    main()
