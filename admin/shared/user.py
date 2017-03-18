import sys


class User(object):

    def __init__(self, username: str):
        self.username = username

    def exists(self, cursor) -> bool:

        user_query = "SELECT * FROM users where username=%s limit 1"
        cursor.execute(user_query, (self.username,))
        result = cursor.fetchone()

        if result:
            return True
        else:
            return False

    def delete(self, cursor, connection) -> bool:
        # TODO: delete all old bets and other user state

        user_query = "SELECT id FROM users where username=%s limit 1"
        cursor.execute(user_query, (self.username,))
        user_id = cursor.fetchone()[0]

        delete_bank = "DELETE FROM banks WHERE type='user' and entity_id=%s"
        delete_user = "DELETE FROM users WHERE id=%s"

        try:
            cursor.execute(delete_bank, (user_id,))

            delete_row_count = cursor.rowcount
            if delete_row_count != 1:
                raise Exception("Bank deletion query ran with %d effected rows. Aborting.." % delete_row_count)

            cursor.execute(delete_user, (user_id,))
            delete_user_count = cursor.rowcount
            if delete_user_count != 1:
                raise Exception("User deletion query ran with %d effected rows. Aborting.." % delete_user_count)

        except Exception as e:
            sys.stderr.write("\nDelete action failed with exception: %s\n" % e)
            connection.rollback()
            return False

        connection.commit()
        return True
