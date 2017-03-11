import unittest
from unittest.mock import MagicMock

from admin.close_poll import divide_pool
from admin.shared.transaction import Transaction


def check_equal(l1, l2):
    return len(l1) == len(l2) and sorted(l1) == sorted(l2)


class TestDividePool(unittest.TestCase):

    def setUp(self):

        self.mock_cursor = MagicMock()
        self.mock_conn = MagicMock()

    def test_divide_pool_happy(self):
        POOL_BANK_ID = 14
        CHOICE_SET = [21, 22, 23]
        USER_IDS = [1, 2, 3, 4, 5]
        USER_BANK_IDS = [101, 102, 103, 104, 105]

        self.mock_cursor.fetchone.side_effect = [
            ("poll1", True, 40),
            (POOL_BANK_ID, 200)
        ]

        self.mock_cursor.fetchall.side_effect = [
            [
                (1, 21, 101),
                (2, 22, 102),
                (3, 22, 103),
                (4, 23, 104),
                (5, 21, 105),
            ]
        ]

        result = divide_pool(10, 22, self.mock_cursor, self.mock_conn)

        user1_transaction = Transaction(14, 101, 'payout', 0)
        user2_transaction = Transaction(14, 102, 'payout', 100)
        user3_transaction = Transaction(14, 103, 'payout', 100)
        user4_transaction = Transaction(14, 104, 'payout', 0)
        user5_transaction = Transaction(14, 105, 'payout', 0)

        expected_transactions = [user1_transaction, user2_transaction, user3_transaction,
                                 user4_transaction, user5_transaction]

        self.assertTrue(check_equal(expected_transactions, result))

    def test_divide_pool_uneven(self):
        POOL_BANK_ID = 14
        CHOICE_SET = [21, 22, 23]
        USER_IDS = [1, 2, 3, 4, 5]
        USER_BANK_IDS = [101, 102, 103, 104, 105]

        self.mock_cursor.fetchone.side_effect = [
            ("poll1", True, 35),
            (POOL_BANK_ID, 245)
        ]

        self.mock_cursor.fetchall.side_effect = [
            [
                (1, 21, 101),
                (2, 22, 102),
                (3, 22, 103),
                (4, 23, 104),
                (5, 21, 105),
                (6, 21, 106),
                (7, 21, 107)
            ]
        ]

        result = divide_pool(10, 22, self.mock_cursor, self.mock_conn)

        user1_transaction = Transaction(14, 101, 'payout', 0)
        user2_transaction = Transaction(14, 102, 'payout', 122)
        user3_transaction = Transaction(14, 103, 'payout', 123)
        user4_transaction = Transaction(14, 104, 'payout', 0)
        user5_transaction = Transaction(14, 105, 'payout', 0)
        user6_transaction = Transaction(14, 106, 'payout', 0)
        user7_transaction = Transaction(14, 107, 'payout', 0)

        expected_transactions = [user1_transaction, user2_transaction, user3_transaction,
                                 user4_transaction, user5_transaction, user6_transaction,
                                 user7_transaction]

        self.assertTrue(check_equal(expected_transactions, result))

    def test_divide_pool_uneven_5(self):
        POOL_BANK_ID = 14
        CHOICE_SET = [21, 22, 23]
        USER_IDS = [1, 2, 3, 4, 5]
        USER_BANK_IDS = [101, 102, 103, 104, 105]

        self.mock_cursor.fetchone.side_effect = [
            ("poll1", True, 45),
            (POOL_BANK_ID, 225)
        ]

        self.mock_cursor.fetchall.side_effect = [
            [
                (1, 21, 101),
                (2, 22, 102),
                (3, 22, 103),
                (4, 22, 104),
                (5, 22, 105),

            ]
        ]

        result = divide_pool(10, 22, self.mock_cursor, self.mock_conn)

        user1_transaction = Transaction(14, 101, 'payout', 0)
        user2_transaction = Transaction(14, 102, 'payout', 56)
        user3_transaction = Transaction(14, 103, 'payout', 57)
        user4_transaction = Transaction(14, 104, 'payout', 56)
        user5_transaction = Transaction(14, 105, 'payout', 56)

        expected_transactions = [user1_transaction, user2_transaction, user3_transaction,
                                 user4_transaction, user5_transaction]

        self.assertTrue(check_equal(expected_transactions, result))

    def test_divide_pool_two_winners(self):
        POOL_BANK_ID = 14
        CHOICE_SET = [21, 22, 23]
        USER_IDS = [1, 2, 3, 4, 5]
        USER_BANK_IDS = [101, 102, 103, 104, 105]

        self.mock_cursor.fetchone.side_effect = [
            ("poll1", True, 100),
            (POOL_BANK_ID, 200)
        ]

        self.mock_cursor.fetchall.side_effect = [
            [
                (1, 22, 101),
                (2, 22, 102),
            ]
        ]

        result = divide_pool(10, 22, self.mock_cursor, self.mock_conn)

        user1_transaction = Transaction(14, 101, 'payout', 100)
        user2_transaction = Transaction(14, 102, 'payout', 100)
        expected_transactions = [user1_transaction, user2_transaction]

        self.assertTrue(check_equal(expected_transactions, result))

    def test_divide_pool_one_winner(self):
        POOL_BANK_ID = 14
        CHOICE_SET = [21, 22, 23]
        USER_IDS = [1, 2, 3, 4, 5]
        USER_BANK_IDS = [101, 102, 103, 104, 105]

        self.mock_cursor.fetchone.side_effect = [
            ("poll1", True, 100),
            (POOL_BANK_ID, 100)
        ]

        self.mock_cursor.fetchall.side_effect = [
            [
                (1, 22, 101),
            ]
        ]

        result = divide_pool(10, 22, self.mock_cursor, self.mock_conn)

        user1_transaction = Transaction(14, 101, 'payout', 100)
        expected_transactions = [user1_transaction]

        self.assertTrue(check_equal(expected_transactions, result))

    def test_divide_pool_no_winners(self):
        POOL_BANK_ID = 14
        CHOICE_SET = [21, 22, 23]
        USER_IDS = [1, 2, 3, 4, 5]
        USER_BANK_IDS = [101, 102, 103, 104, 105]

        self.mock_cursor.fetchone.side_effect = [
            ("poll1", True, 30),
            (POOL_BANK_ID, 120)
        ]

        self.mock_cursor.fetchall.side_effect = [
            [
                (1, 21, 101),
                (2, 23, 102),
                (3, 21, 103),
                (4, 25, 104),
            ]
        ]

        result = divide_pool(10, 22, self.mock_cursor, self.mock_conn)

        user1_transaction = Transaction(14, 101, 'payout', 30)
        user2_transaction = Transaction(14, 102, 'payout', 30)
        user3_transaction = Transaction(14, 103, 'payout', 30)
        user4_transaction = Transaction(14, 104, 'payout', 30)

        expected_transactions = [user1_transaction, user2_transaction, user3_transaction,
                                 user4_transaction]

        self.assertTrue(check_equal(expected_transactions, result))




