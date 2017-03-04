import argparse
import psycopg2
import sys
import time
import yaml

from typing import List

yes = {'yes', 'y', 'ye'}
no = {'no', 'n', ''}


class Transaction(object):

    def __init__(self, from_id: int, to_id: int, category: str, amount: int) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.category = category
        self.amount = amount

    def __str__(self):
        return "from: %d to: %d for balance: %d" % (self.from_id, self.to_id, self.amount)


def send_transactions(poll_id: int, transactions: List[Transaction], cursor, connection):
    """
    this method takes transactions, puts them into the db and marks the poll as paid out.
    it also asks you to verify
    :param poll_id:
    :param transactions:
    :param cursor:
    :param connection:
    :return:
    """

    total = 0
    sys.stdout.write("\n\nThese are the transactions that are going to be written to the db:\n")
    for idx, transaction in enumerate(transactions):
        sys.stdout.write("%d) %s\n" % (idx+1, str(transaction)))
        total += transaction.amount

    sys.stdout.write("A total of %d coins are going to sent from the poll.\n\n" % total)
    result = input("Does this look correct to you? ")

    if result in no:
        sys.stderr.write("\nUser-initiated abort. Closing..\n\n")
        sys.exit()
    elif result in yes:
        pass
    else:
        sys.stderr.write("\nPlease respond with 'yes' or 'no'.\n\n")
        sys.exit()

    print("bomb")


def divide_pool(poll_id: int, correct_id: int, cursor, conn) -> List[Transaction]:
    """
    this method collects all the bets and divides up
    :param poll_id: integer poll id
    :param correct_id: int choice id
    :param cursor: psycopg2 cursor
    :param conn: psycopg2 connection
     :return: list of transaction objects
    """
    poll_query = "SELECT title, finished, buy_in FROM polls WHERE id=%d" % poll_id
    cursor.execute(poll_query)
    poll_result = cursor.fetchone()
    poll_buyin = poll_result[2]

    banks_query = "SELECT id, balance FROM banks WHERE entity_id=%d and type='poll' limit 1" % poll_id
    cursor.execute(banks_query)
    bank_result = cursor.fetchone()

    poll_bank_id = bank_result[0]
    balance_pool_size = bank_result[1]

    transactions_query = "SELECT user_id, choice_id, banks.id FROM bets left join banks on " \
                         "banks.entity_id=bets.user_id where banks.type='user' and poll_id=%d" % poll_id
    cursor.execute(transactions_query)
    transactions_results = cursor.fetchall()

    pool_size = len(transactions_results) * poll_buyin

    print("balance pool size: %d" % balance_pool_size)
    print("pool size: %d" % pool_size)

    if pool_size != balance_pool_size:
        print("the balance records don't match.. womp womp")
        raise Exception("transaction mismatch")

    answer_sums = {}
    payout_map = {}  # a dict with bank ids with their respective balances
    payout_array = []

    for bet in transactions_results:
        answer_sums[bet[1]] = answer_sums.get(bet[1], 0) + 1

        if bet[1] == correct_id:
            payout_map[bet[2]] = 0
            payout_array.append(bet[2])

    for coin in range(1, pool_size+1):
        bank_id = payout_array[coin % len(payout_array)]
        payout_map[bank_id] += 1

    print(payout_map)

    new_total = 0
    transactions = []
    for key in payout_map:
        new_transactions = Transaction(poll_bank_id, key, 'payout', payout_map[key])
        new_total += payout_map[key]
        transactions.append(new_transactions)

    if new_total != pool_size:
        sys.stderr.write("transactions distribution doesn't match up.. expected %d but got %d" % (
            pool_size, new_total
        ))
    return transactions


def validate(poll_id, correct_id, cursor, conn):

    poll_query = "SELECT title, finished, buy_in FROM polls WHERE id=%d" % poll_id
    cursor.execute(poll_query)
    result = cursor.fetchone()

    if not result[1]:
        sys.stderr.write("Poll isn't closed yet. \n")
        return False

    choices_query = "SELECT id, title FROM poll_answers WHERE poll_id=%d" % poll_id
    cursor.execute(choices_query)
    choices = cursor.fetchall()

    print("\nQuestion: %s" % result[0])
    for idx, choice in enumerate(choices):
        if choice[0] == correct_id:
            selected = "- SELECTED"
        else:
            selected = ""
        print("%d) %s%s" % (idx+1, choice[1], selected))

    test = input("\nDoes this look correct to you? [y/n] ").lower()

    if test in yes:
        return True
    elif test in no:
        return False
    else:
        sys.stderr.write("\nPlease respond with 'yes' or 'no'.\n\n")
        sys.exit()


with open('db.yml', 'r') as stream:
    try:
        print("loading db config from yml")
        db_config = yaml.load(stream)['db_creds']
    except yaml.YAMLError as e:
        print(e)
        print('unable to load yaml')
        sys.exit()

connection = psycopg2.connect(database=db_config['database'],
                              user=db_config['user'],
                              password=db_config['password'],
                              host=db_config['host'],
                              port=db_config['port'])
cursor = connection.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("poll_id", help="id of poll to close")
parser.add_argument("choice_id", help="id of choice to close")

args = parser.parse_args()

poll_id = int(args.poll_id)
choice_id = int(args.choice_id)

# TODO: query for title and answer

is_valid = validate(poll_id, choice_id, cursor, connection)

if not is_valid:
    sys.stdout.write("Please correct your input data.\n\n")
    sys.exit()

transactions = divide_pool(poll_id, choice_id, cursor, connection)

result = send_transactions(poll_id, transactions, cursor, connection)






