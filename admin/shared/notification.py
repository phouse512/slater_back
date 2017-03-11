from admin.shared.transaction import Transaction


class Notification(object):
    """
    the class responsible for representing an individual message
    """

    def __init__(self, user_id: int, message: str) -> None:
        self.user_id = user_id
        self.message = message

    @staticmethod
    def from_transaction(transaction: Transaction, cursor, connection):
        """
            logic to generate notification from transaction
        """

        if transaction.category == 'payout':
            user_bank_id = transaction.to_id
        else:
            return None

        user_id_query = "SELECT entity_id FROM banks WHERE id=%s and type='user'"
        cursor.execute(user_id_query, (user_bank_id,))
        user_id = cursor.fetchone()[0]

        if transaction.amount > 0:
            message = "You just won %d coins from your latest bet!" % transaction.amount
        else:
            message = "You didn't win anything from your latest bet :("

        return Notification(user_id, message)
