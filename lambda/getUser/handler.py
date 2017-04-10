import boto3
import json
import os
import psycopg2
import telnetlib

s3 = boto3.client('s3')


def lambda_handler(event, context):

    print(telnetlib.Telnet(os.environ['host'], os.environ['port']))

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    user_id = int(event['requestContext']['authorizer']['principalId'])

    user_query = "SELECT users.id, username, banks.balance FROM users left join banks on banks.entity_id=users.id " \
                 " where users.id=%d and banks.type='user' limit 1" % user_id
    cursor.execute(user_query)
    result = cursor.fetchone()

    if not result:
        return {
            'statusCode': 404,
            'headers': {},
            'body': json.dumps({'error': 'User not found'})
        }

    return_object = {
        'id': user_id,
        'balance': result[2],
        'username': result[1]
    }

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(return_object)
    }
