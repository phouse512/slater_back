import boto3
import json
import os
import psycopg2

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    user_id = int(event['requestContext']['authorizer']['principalId'])
    poll_id = int(event['pathParameters']['poll_id'])

    incoming_object = json.loads(event['body'])
    answer_id = int(incoming_object['answer_id'])

    """
        this chunk of code is responsible for querying the poll, making sure it is valid,
        and getting it's bank account so we can use it later if necessary
    """
    poll_query = "select polls.id as poll, banks.id as bank, banks.balance as balance, is_pre, close_time, buy_in, finished from polls " \
                 "left join banks on banks.entity_id=polls.id where polls.id=%d and banks.type='poll' and " \
                 "polls.is_pre=false and polls.finished=false" % poll_id
    cursor.execute(poll_query)
    poll_result = cursor.fetchone()

    if not poll_result:
        # poll doesn't exist that meets these criteria
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({"error": "invalid poll for id: %d" % poll_id})
        }

    # TODO: assert that given answer id is a valid choice

    poll_bank_id = poll_result[1]
    poll_buyin = poll_result[5]
    poll_bank_balance = poll_result[2]

    """
        this chunk of code grabs the user's bank account (we know the user exists because
        of the authorizer) so that we can use it later if necessary
    """
    user_query = "select banks.id, banks.balance from banks where entity_id=%d and type='user' " \
                 "limit 1" % user_id
    cursor.execute(user_query)
    user_bank_result = cursor.fetchone()

    if not user_bank_result:
        # bank account doesn't exist, that's bad
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({"error": "no bank account exists for user: %d" % user_id})
        }

    user_bank_id = user_bank_result[0]
    user_bank_balance = user_bank_result[1]

    """
        now we have validated what we needed to do, and are sure that both users/bank accounts
        and polls exist. time for the bet logic.

        if there is an existing bet, simply change the choice_id in their bet, the money
        transaction has already been made so it is not necessary here. still return the transaction id

        otherwise, create a new transaction and a new bet object, rolling back if there is an
        error so that transactions don't get made without a bet
    """
    existing_bet_query = "SELECT id, choice_id FROM bets WHERE poll_id=%d and user_id=%d limit 1" % (
        poll_id, user_id
    )
    cursor.execute(existing_bet_query)

    try:

        result = cursor.fetchone()
        if result:
            print("shouldn't be here")
            bet_id = result[0]
            # there is an existing bet, don't need to make a new transaction, just update the bet
            update_bet_query = "UPDATE bets set choice_id=%d WHERE id=%d" % (answer_id, bet_id)
            cursor.execute(update_bet_query)

            existing_money_query = "SELECT id FROM transactions WHERE from_entity=%d and to_entity=%d and " \
                                   "type='bet' LIMIT 1" % (user_bank_id, poll_bank_id)
            cursor.execute(existing_money_query)
            existing_money_res = cursor.fetchone()
            transaction_id = existing_money_res[0]

            new_user_balance = user_bank_balance

        else:
            # make a new transaction
            # TODO: add transaction_id to bets table

            insert_bet_query = "INSERT INTO bets (user_id, poll_id, choice_id) values " \
                               "(%d, %d, %d) returning id" % (user_id, poll_id, answer_id)

            insert_money_query = "INSERT INTO transactions (from_entity, to_entity, balance, type) " \
                                 "values (%d, %d, %d, 'bet') returning id" % (user_bank_id, poll_bank_id, poll_buyin)

            cursor.execute(insert_bet_query)
            bet_id = cursor.fetchone()[0]

            cursor.execute(insert_money_query)
            transaction_id = cursor.fetchone()[0]

            # update new user balance
            update_balance_query = "UPDATE banks SET balance=%d WHERE id=%d" % (
                user_bank_balance - poll_buyin, user_bank_id
            )

            update_poll_balance_qs = "UPDATE banks SET balance=%d WHERE id=%d" % (
                poll_bank_balance + poll_buyin, poll_bank_id
            )

            new_user_balance = user_bank_balance - poll_buyin

            cursor.execute(update_balance_query)
            cursor.execute(update_poll_balance_qs)

    except Exception as e:
        connection.rollback()
        print(e)
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'error': 'Error within sql transactions, rolling back'})
        }
        # return error

    connection.commit()

    return_object = {
        'transaction_id': transaction_id,
        'bet_id': bet_id,
        'new_balance': new_user_balance
    }

    return {
        'statusCode': 400,
        'headers': {},
        'body': json.dumps(return_object)
    }
