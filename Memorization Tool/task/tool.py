from string import Template

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

WRONG = "WRONG OPTION\n"
FLASHCARDS_MAIN_MENU = "1. Add a new flashcard\n2. Exit\n"
FLASHCARD_UPDATE_MENU = '''press "d" to delete the flashcard:
press "e" to edit the flashcard:'''
FLASHCARDS_NAVIGATION_OPTIONS = '''press "y" to see the answer:
press "n" to skip:
press "u" to update:\n'''

BOX_UPDATE_OPTIONS = '''press "y" if your answer is correct:
press "n" if your answer is wrong:'''

error_msg_template = Template("$value is not an option")
flashcard_value_template = Template('''current $key_name: $key_value
please write a new $key_name:\n''')


Base = declarative_base()


class FlashCards(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String(200))
    answer = Column(String(200))
    box = Column(Integer, default=1)


class MemorizationTool:

    @staticmethod
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

    def flashcards_menu(self):
        while True:
            _option = input(FLASHCARDS_MAIN_MENU)
            match _option:
                case "1":
                    MemorizationTool.add_flashcard()
                case "2":
                    return self.menu()
                case _:
                    print(error_msg_template.substitute(value=_option))

    @staticmethod
    def update_flashcard(session, query, row):
        _choice = None
        while _choice not in {"d", "e"}:
            _choice = input(FLASHCARD_UPDATE_MENU)
            match _choice:
                case "d":
                    session.delete(row)
                case "e":
                    print(flashcard_value_template.substitute(
                        key_name="question",
                        key_value=row.question
                    )
                    )
                    new_question = input()

                    print(flashcard_value_template.substitute(
                        key_name="answer",
                        key_value=row.answer
                    )
                    )

                    new_answer = input()
                    if all([new_question, new_answer]):
                        _filter = query.filter(FlashCards.id == row.id)
                        _filter.update({"question": new_question,
                                        "answer": new_answer}
                                       )
                case _:
                    print(error_msg_template.substitute(value=_choice))
        session.commit()

    @staticmethod
    def update_box_num(session, query, row):
        option = None
        id_filter = query.filter(FlashCards.id == row.id)

        while option not in {"y", "n"}:
            option = input(BOX_UPDATE_OPTIONS)
        match option:
            case "y":
                if row.box == 3:
                    session.delete(row)
                else:
                    id_filter.update({'box': row.box + 1})
            case "n":
                if row.box in {2, 3}:
                    id_filter.update({'box': row.box - 1})
        session.commit()

    @staticmethod
    def practice_flashcards():

        session = Session()
        query = session.query(FlashCards)
        result_list = query.all()
        if not result_list:
            print("There is no flashcard to practice!")
        else:
            for row in result_list:
                print(f"Question: {row.question}")
                answer = input(FLASHCARDS_NAVIGATION_OPTIONS).lower()
                match answer:
                    case "y":
                        print(f"Answer: {row.answer}")
                        MemorizationTool.update_box_num(session, query, row)
                    case "n":
                        pass
                    case "u":
                        MemorizationTool.update_flashcard(session, query, row)

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
