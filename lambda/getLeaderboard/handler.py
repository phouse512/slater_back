import boto3
import json
import os
import psycopg2

s3 = boto3.client('s3')


def lambda_handler(event, context):

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])

    cursor = connection.cursor()
    leaderboard_query = "select users.id, users.username, banks.balance from users left join banks on " \
                        "banks.entity_id=users.id where banks.type='user' order by banks.balance desc"

    cursor.execute(leaderboard_query)
    results = cursor.fetchall()

    all_users = []
    for leader in results:
        all_users.append({
            'id': leader[0],
            'username': leader[1],
            'balance': leader[2]
        })

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(all_users)
    }
