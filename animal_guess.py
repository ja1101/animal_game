from animal import get_random_animal
from glm import call_gpt

def main():
    animal = get_random_animal()
    print(animal)
    while True:
        q = input("Ask a yes or no question to guess the animal: ")
        if animal in q:
            print("Correct!")
            return
        gpt_resp = call_gpt("For animal " + animal + ", answer with yes or no: " + q)
        print(gpt_resp["content"])

if __name__ == "__main__":
    main()
