from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker


WRONG = "WRONG OPTION\n"

Base = declarative_base()


class FlashCards(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


class MemorizationTool:

    def flashcards_menu(self):
        def add_flashcard():
            question = None
            answer = None

            while not question:
                question = input("Question:\n").strip()
            while not answer:
                answer = input("Answer:\n").strip()

            new_flashcard = FlashCards(question=question, answer=answer)
            session = Session()
            session.add(new_flashcard)
            session.commit()  # session will be terminated after comit command

        while True:
            _option = input("1. Add a new flashcard\n2. Exit\n")
            match _option:
                case "1":
                    add_flashcard()
                case "2":
                    return self.menu()
                case _:
                    print(f"{_option} is not an option")

    @staticmethod
    def practice_flashcards():
        session = Session()

        result_list = session.query(FlashCards)
        if not result_list:
            print("There is no flashcard to practice!")

        else:
            for row in result_list:
                print(f"Question: {row.question}")
                print('Please press "y" to see the answer or press "n" to skip:')
                answer = input().lower()
                match answer:
                    case "y":
                        print(f"Answer: {row.answer}")
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
    engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    MemorizationTool().menu()
