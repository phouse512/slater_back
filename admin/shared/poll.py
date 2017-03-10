import sys

from typing import Any, Dict, List


class Answer(object):

    def __init__(self, answer_text: str) -> None:

        self.answer_text = answer_text


class Poll(object):

    def __init__(self, question: str, buy_in: int, close_time: int, answers: List[Answer]) -> None:

        self.question = question  # type: str
        self.buy_in = buy_in  # type: int
        self.close_time = close_time  # type: int
        self.answers = answers  # type: List[Answer]

    @staticmethod
    def load_from_yaml(yaml_obj: Dict[Any, Any]):

        question = yaml_obj['question']
        buy_in = yaml_obj['buy_in']
        close_time = yaml_obj['close_time']

        answers = []
        for answer in yaml_obj['answers']:
            answers.append(Answer(answer))

        return Poll(question, buy_in, close_time, answers)

    def store_poll(self, cursor, connection):
        sys.stdout.write("Storing for poll: %s with buy-in: %d and close time: %d\n" % (
            self.question, self.buy_in, self.close_time
        ))

        store_query = "INSERT INTO polls (title, buy_in, close_time) VALUES (%s, %s, to_timestamp(%s)) " \
                      "returning id"

        cursor.execute(store_query, (self.question, self.buy_in, self.close_time))
        poll_id = cursor.fetchone()[0]

        answers_tuple = []
        for answer in self.answers:
            answers_tuple.append((str(poll_id), str(answer.answer_text),))

        # add poll answers
        answer_args_str = b','.join(cursor.mogrify(b'(%s, %s)', x) for x in answers_tuple)
        cursor.execute(b"INSERT INTO poll_answers (poll_id, title) VALUES " + answer_args_str)

        # add bank account for poll
        bank_query = "INSERT INTO banks (type, entity_id, balance) VALUES (%s, %s, %s)"
        cursor.execute(bank_query, ('poll', poll_id, 0,))

        connection.commit()
