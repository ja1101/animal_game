from animal import get_random_animal
from glm import call_gpt
from re import split

def main():
    animal = get_random_animal()
    print(animal)
    gpt_resp = call_gpt("Play 20 questions. " + 
    "I am thinking of a type of animal (e.g. dog). Your task will be to guess which type it is " +
    "by asking yes or no questions back to me. So, ask your first question.")
    resp = gpt_resp["content"]
    print(resp)
    while True:
        if animal in split(r"\W+", resp.lower()):
            print("Correct guess from AI!")
            #return
        q = input("Respond yes or no to AI: ").lower()
        if "give up" in q:
            print("The animal was: " + animal)
            return
        gpt_resp = call_gpt(f"your response was {gpt_resp} - " + f"The answer to your question is {q}. " +
        "Now ask your next question based on the information you have so far.")
        resp = gpt_resp["content"]
        print(resp)

if __name__ == "__main__":
    print(call_gpt("Which model are you?")["content"])
    main()
