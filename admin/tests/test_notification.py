import unittest

from admin.shared.notification import Notification
from admin.shared.transaction import Transaction
from unittest.mock import MagicMock


class NotificationTests(unittest.TestCase):

    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()

        self.user_bank_id = 10
        self.poll_bank_id = 12

    def test_from_transaction(self):
        test_transaction = Transaction(self.poll_bank_id, self.user_bank_id, 'payout', 121)
        self.mock_cursor.fetchone.side_effect = [[21]]

        notification = Notification.from_transaction(test_transaction, self.mock_cursor,
                                                     self.mock_connection)

        self.mock_cursor.execute.assert_called_once_with("SELECT entity_id FROM banks WHERE id=%s and type='user'",
                                                 (self.user_bank_id,))
        self.assertEqual(21, notification.user_id)
        self.assertEqual("You just won 121 coins from your latest bet!", notification.message)

    def test_from_user_transaction(self):
        test_transaction = Transaction(self.user_bank_id, self.poll_bank_id, 'bet', 130)

        notification = Notification.from_transaction(test_transaction, self.mock_cursor,
                                                     self.mock_connection)

        self.assertIsNone(notification)
        self.mock_cursor.execute.assert_not_called()
