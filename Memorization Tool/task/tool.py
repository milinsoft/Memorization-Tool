from string import Template

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

WRONG = "WRONG OPTION\n"
error_msg_template = Template("$value is not an option")
new_value_template = Template("current $var: $value\n"
                              "please write a new $var:\n")

Base = declarative_base()


class FlashCards(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer, default=1)


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
            _option = input("1. Add a new flashcard\n"
                            "2. Exit\n")
            match _option:
                case "1":
                    add_flashcard()
                case "2":
                    return self.menu()
                case _:
                    print(error_msg_template.substitute(value=_option))

    @staticmethod
    def update_flashcard(session, query, row):
        _choice = None
        while not _choice:
            _choice = input('press "d" to delete the flashcard:\n'
                            'press "e" to edit the flashcard:')
            match _choice:
                case "d":
                    session.delete(row)
                    session.commit()
                case "e":

                    new_question = input(f"current question: {row.question}\n"
                                         "please write a new question:\n")

                    new_answer = input(f"current answer: {row.answer}\n"
                                       "please write a new answer:\n")
                    if all([new_question and new_answer]):
                        _filter = query.filter(FlashCards.id == row.id)
                        _filter.update({"question": new_question,
                                        "answer": new_answer}
                                       )
                case _:
                    _choice = None  # reseting to None & continue the loop
                    print(error_msg_template.substitute(value=_choice))
        session.commit()

    @staticmethod
    def update_box_num(session, query, row):
        option = None
        while option not in {"y", "n"}:
            option = input('press "y" if your answer is correct:\n'
                           'press "n" if your answer is wrong:')
        match option:
            case "y":
                ...
                if row.box == 3:
                    session.delete(row)
                else:
                    id_filter = query.filter(FlashCards.id == row.id)
                    id_filter.update({'box': row.box + 1})

            case "n":
                if row.box in {2, 3}:
                    id_filter = query.filter(FlashCards.id == row.id)
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
                msg = 'press "y" to see the answer:\n' \
                      'press "n" to skip:\n' \
                      'press "u" to update:'
                answer = input(msg).lower()
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
