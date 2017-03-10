import unittest

from admin.add_poll import load_polls
from admin.add_poll import validate_polls
from admin.shared.poll import Answer
from admin.shared.poll import Poll
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch


class AddPollsTest(unittest.TestCase):

    def setUp(self):
        self.test_input_yml = "admin/tests/test_input_cases.yml"

        poll1 = Poll("Wed, Mar 8 Celtics vs. Warriors", 40, 1489258327,
                     [Answer("Celtics"), Answer("Warriors")])

        poll2 = Poll("Wed, Mar 8 Jazz vs. Rockets", 40, 1489258327,
                     [Answer("Jazz"), Answer("Rockets")])

        poll3 = Poll("How many 3's will Steph Curry attempt?", 40, 1489258327,
                     [Answer("less than 5"), Answer("5-8"),
                      Answer("9, 10, or 11"), Answer("12 or more")])

        self.test_polls = [poll1, poll2, poll3]

        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()

    def test_load_polls(self):

        result = load_polls(self.test_input_yml)

        self.assertEqual("Wed, Mar 8 Celtics vs. Warriors", result[0].question)
        self.assertEqual(40, result[0].buy_in)
        self.assertEqual(1489258327, result[0].close_time)
        self.assertEqual("Celtics", result[0].answers[0].answer_text)
        self.assertEqual("Warriors", result[0].answers[1].answer_text)

        self.assertEqual("Wed, Mar 8 Jazz vs. Rockets", result[1].question)
        self.assertEqual(40, result[1].buy_in)
        self.assertEqual(1489258327, result[1].close_time)
        self.assertEqual("Jazz", result[1].answers[0].answer_text)
        self.assertEqual("Rockets", result[1].answers[1].answer_text)

        self.assertEqual("How many 3's will Steph Curry attempt?", result[2].question)
        self.assertEqual(50, result[2].buy_in)
        self.assertEqual(1489258327, result[2].close_time)
        self.assertEqual("less than 5", result[2].answers[0].answer_text)
        self.assertEqual("5-8", result[2].answers[1].answer_text)
        self.assertEqual("9, 10, or 11", result[2].answers[2].answer_text)
        self.assertEqual("12 or more", result[2].answers[3].answer_text)

    @patch("time.time")
    @patch("sys.stdout")
    def test_validate_polls_all_valid(self, stdout_mock, time_mock):

        time_mock.side_effect = [1489208327]
        self.mock_cursor.fetchone.side_effect = [None, None, None]

        resulting_polls = validate_polls(self.test_polls, self.mock_cursor, self.mock_connection)

        select_calls = [
            call("SELECT * from polls where title=%s", ("Wed, Mar 8 Celtics vs. Warriors",)),
            call("SELECT * from polls where title=%s", ("Wed, Mar 8 Jazz vs. Rockets",)),
            call("SELECT * from polls where title=%s", ("How many 3's will Steph Curry attempt?",))
        ]

        self.mock_cursor.execute.assert_has_calls(select_calls, any_order=False)
        self.assertEqual(3, len(resulting_polls))
        self.assertEqual(self.test_polls[0].question, resulting_polls[0].question)
        self.assertEqual(self.test_polls[1].question, resulting_polls[1].question)
        self.assertEqual(self.test_polls[2].question, resulting_polls[2].question)

    @patch("time.time")
    @patch("sys.stderr")
    def test_validate_polls_some_exist(self, stderr_mock, time_mock):

        time_mock.side_effect = [1489208327]
        self.mock_cursor.fetchone.side_effect = [None, 1, 1]

        resulting_polls = validate_polls(self.test_polls, self.mock_cursor, self.mock_connection)

        select_calls = [
            call("SELECT * from polls where title=%s", ("Wed, Mar 8 Celtics vs. Warriors",)),
            call("SELECT * from polls where title=%s", ("Wed, Mar 8 Jazz vs. Rockets",)),
            call("SELECT * from polls where title=%s", ("How many 3's will Steph Curry attempt?",))
        ]

        write_calls = [
            call("Poll with title: Wed, Mar 8 Jazz vs. Rockets  already exists, skipping\n"),
            call("Poll with title: How many 3's will Steph Curry attempt?  already exists, skipping\n"),
        ]

        stderr_mock.write.assert_has_calls(write_calls, any_order=False)
        self.mock_cursor.execute.assert_has_calls(select_calls, any_order=False)
        self.assertEqual(1, len(resulting_polls))
        self.assertEqual(self.test_polls[0].question, resulting_polls[0].question)

    @patch("time.time")
    @patch("sys.stderr")
    def test_validate_polls_too_close(self, stderr_mock, time_mock):

        time_mock.side_effect = [1489258000]
        self.mock_cursor.fetchone.side_effect = [None, None, None]

        resulting_polls = validate_polls(self.test_polls, self.mock_cursor, self.mock_connection)

        select_calls = [
            call("SELECT * from polls where title=%s", ("Wed, Mar 8 Celtics vs. Warriors",)),
            call("SELECT * from polls where title=%s", ("Wed, Mar 8 Jazz vs. Rockets",)),
            call("SELECT * from polls where title=%s", ("How many 3's will Steph Curry attempt?",))
        ]

        write_calls = [
            call("Poll with close time: 1489258327 is in the past or less than 30 minutes from now, skipping\n"),
            call("Poll with close time: 1489258327 is in the past or less than 30 minutes from now, skipping\n"),
            call("Poll with close time: 1489258327 is in the past or less than 30 minutes from now, skipping\n"),

        ]

        stderr_mock.write.assert_has_calls(write_calls, any_order=False)
        self.mock_cursor.execute.assert_has_calls(select_calls, any_order=False)
        self.assertEqual(0, len(resulting_polls))
