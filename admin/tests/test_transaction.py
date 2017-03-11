import unittest

from admin.shared.transaction import Transaction


class TransactionTests(unittest.TestCase):

    def setUp(self):
        self.from_id = 31
        self.to_id = 21
        self.category = 'bet'
        self.amount = 50

    def test_transaction_constructor(self):

        transaction = Transaction(self.from_id, self.to_id, self.category, self.amount)

        self.assertEqual(self.from_id, transaction.from_id)
        self.assertEqual(self.to_id, transaction.to_id)
        self.assertEqual(self.category, transaction.category)
        self.assertEqual(self.amount, transaction.amount)

    def test_generate_sql(self):

        transaction = Transaction(self.from_id, self.to_id, self.category, self.amount)

        result = transaction.generate_sql()

        self.assertEqual("INSERT INTO transactions (from_entity, to_entity, type, balance) "
                         "values (31, 21, 'bet', 50)", result)

    def test_batch_generate_sql(self):
        transaction = Transaction(self.from_id, self.to_id, self.category, self.amount)

        result = transaction.generate_sql(is_batch=True)
        self.assertEqual("(31, 21, 'bet', 50)", result)

    def test_create_list_sql(self):

        transaction1 = Transaction(self.from_id, self.to_id, self.category, self.amount)
        transaction2 = Transaction(self.from_id, self.to_id, self.category, self.amount)
        transaction3 = Transaction(self.from_id, self.to_id, self.category, self.amount)

        all_transactions = [transaction1, transaction2, transaction3]

        result = Transaction.create_list_sql(all_transactions)

        expected_result = "INSERT INTO transactions (from_entity, to_entity, type, balance) values " \
                          "(31, 21, 'bet', 50), (31, 21, 'bet', 50), (31, 21, 'bet', 50)"
        self.assertEqual(expected_result, result)

    def test_create_single_list(self):

        transaction1 = Transaction(self.from_id, self.to_id, self.category, self.amount)
        all_transactions = [transaction1]

        result = Transaction.create_list_sql(all_transactions)

        expected_result = "INSERT INTO transactions (from_entity, to_entity, type, balance) values " \
                          "(31, 21, 'bet', 50)"
        self.assertEqual(expected_result, result)

if __name__ == '__main__':

    unittest.main()
