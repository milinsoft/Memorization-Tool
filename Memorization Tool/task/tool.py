from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from string import Template

WRONG = "WRONG OPTION\n"
error_msg_template = Template("$value is not an option")

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
                    print(error_msg_template.substitute(value=_option))

    @staticmethod
    def practice_flashcards():
        def update_flashcard():
            # updating code
            _choice = None
            while not _choice:
                _choice = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n')
                match _choice:
                    case "d":
                        session.delete(row)
                        session.commit()
                    case "e":
                        new_question = input(f"current question: {row.question}\nplease write a new question:\n")
                        new_answer = input(f"current answer: {row.answer}\nplease write a new answer:\n")
                        if all([new_question and new_answer]):
                            question_filter = query.filter(FlashCards.id == row.id)
                            question_filter.update({"question": new_question,
                                                    "answer": new_answer}
                                                   )
                    case _:
                        _choice = None  # reseting to None and continue the loop
                        print(error_msg_template.substitute(value=_choice))
            session.commit()

        session = Session()
        query = session.query(FlashCards)
        result_list = query.all()
        if not result_list:
            print("There is no flashcard to practice!")

        else:
            for row in result_list:
                print(f"Question: {row.question}")
                answer = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:').lower()
                match answer:
                    case "y":
                        print(f"Answer: {row.answer}")
                    case "n":
                        pass
                    case "u":
                        update_flashcard()

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
                    print(error_msg_template.substitute(value=choice))


if __name__ == '__main__':
    engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    MemorizationTool().menu()
