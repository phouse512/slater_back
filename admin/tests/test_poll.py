import unittest

from admin.shared.poll import Answer
from admin.shared.poll import Poll
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch


class PollsTest(unittest.TestCase):

    def setUp(self):
        self.test_poll = Poll("Who will win?",
                              120,
                              1200,
                              [Answer("answer1"), Answer("answer2")])

        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()

    @patch("sys.stdout")
    def test_store_poll(self, stdout_mock):

        self.mock_cursor.fetchone.side_effect = [[21]]
        self.mock_cursor.mogrify.side_effect = [
            b"(21, 'answer1')",
            b"(21, 'answer2')"
        ]

        self.test_poll.store_poll(self.mock_cursor, self.mock_connection)

        calls = [
            call("INSERT INTO polls (title, buy_in, close_time) VALUES (%s, %s, to_timestamp(%s)) returning id",
                 ("Who will win?", 120, 1200,)),
            call(b"INSERT INTO poll_answers (poll_id, title) VALUES (21, 'answer1'),(21, 'answer2')"),
            call("INSERT INTO banks (type, entity_id, balance) VALUES (%s, %s, %s)",
                 ('poll', 21, 0,))
        ]
        self.mock_cursor.execute.assert_has_calls(calls, any_order=False)
        self.mock_connection.commit.assert_called_with()
        stdout_mock.write.assert_called_with("Storing for poll: Who will win? with buy-in: 120 and close time: 1200\n")
