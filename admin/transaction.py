

class Transaction(object):

    def __init__(self, from_id: int, to_id: int, category: str, amount: int) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.category = category
        self.amount = amount

    def __str__(self):
        return "from: %d to: %d for balance: %d" % (self.from_id, self.to_id, self.amount)

    def __eq__(self, other):
        if self.from_id != other.from_id:
            return False

        if self.to_id != other.to_id:
            return False

        if self.category != other.category:
            return False

        if self.amount != other.amount:
            return False

        return True

    def __lt__(self, other):
        return self.to_id < other.to_id

    @staticmethod
    def create_list_sql(transactions_list):
        """
        this method takes in a list of transactions, and produces the necessary sql to
        insert all of those rows
        """
        base_query = "INSERT INTO transactions (from_entity, to_entity, type, balance) values "

        for idx, transaction in enumerate(transactions_list):
            temp_query = transaction.generate_sql(True)

            if idx < len(transactions_list) -1:
                base_query += temp_query + ", "
            else:
                base_query += temp_query

        return base_query

    def generate_sql(self, is_batch=False):
        """
        return the sql for a single transaction to be used in a list
        """

        if is_batch:
            return "(%d, %d, '%s', %d)" % (self.from_id, self.to_id, self.category, self.amount)
        else:
            return "INSERT INTO transactions (from_entity, to_entity, type, balance) values " \
                   "(%d, %d, '%s', %d)" % (self.from_id, self.to_id, self.category, self.amount)
