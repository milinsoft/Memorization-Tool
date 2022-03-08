# write your code here

WRONG = "WRONG OPTION\n"


class MemorizationTool:

    def __init__(self):
        self.flashcards = {}

    @classmethod
    def from_string(cls):
        pass

    def flashcards_menu(self):
        def add_flashcard():
            question, answer =\
                None, None

            while not question:
                question = input("Question:\n").strip()

            while not answer:
                answer = input("Answer:\n").strip()

            self.flashcards[question] = answer

        while True:
            _option = input("1. Add a new flashcard\n2. Exit\n")
            match _option:
                case "1":
                    add_flashcard()
                case "2":
                    return self.menu()
                case _:
                    print(f"{_option} is not an option")

    def practice_flashcards(self):
        if not self.flashcards:
            print("There is no flashcard to practice!")
        else:
            for question in self.flashcards:
                print(f"Question: {question}")
                print('Please press "y" to see the answer or press "n" to skip:')
                answer = input().lower()
                match answer:
                    case "y":
                        print(f"Answer: {self.flashcards[question]}")
                    case "n":
                        pass

    def menu(self):
        options = "1. Add flashcards\n"\
                  "2. Practice flashcards\n"\
                  "3. Exit\n"

        while True:
            choice = input(options).strip()
            match choice:
                case "1":
                    self.flashcards_menu()
                case "2":
                    self.practice_flashcards()
                case "3":
                    exit(print("Bye!"))
                case _:
                    print(f"{choice} is not an option")


if __name__ == '__main__':
    MemorizationTool().menu()

