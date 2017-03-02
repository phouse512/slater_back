import json
import os
import psycopg2


def lambda_handler(event, context):
    # TODO implement
    print(event)

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    query = "SELECT id, choice_id from bets where poll_id=%d and user_id=%d limit 1" % (
        int(event['pathParameters']['poll_id']),
        int(event['requestContext']['authorizer']['principalId'])
    )
    cursor.execute(query)
    result = cursor.fetchone()

    if not result:
        answer_id = -1

    else:
        answer_id = result[1]

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({ 'answer_id': answer_id})
    }
