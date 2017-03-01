# import bcrypt
import json
import os
import psycopg2


def lambda_handler(event, context):
    # TODO implement
    # print(event['body'])
    # returns {
    #   balance = 431;
    #   id = 2;
    #   username = phouse512
    #}

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    incoming_object = json.loads(event['body'])

    query = "SELECT id, username, created_at, pw_hash from users WHERE username='%s' " \
            "LIMIT 1" % incoming_object["username"]
    cursor.execute(query)

    result = cursor.fetchone()

    if not result:
        return {
            'statusCode': 401,
            'headers': {},
            'body': ''
        }

    hashed_input = "test"
    #hashed_input = bcrypt.hashpw(incoming_object['pw'], result[3])
    if hashed_input != result[3]:
        return {
            'statusCode': 403,
            'headers': {},
            'body': ''
        }

    # now logged in

    auth_object = {
        'auth_token': incoming_object["username"],
        'created_at': '2017-02-26 22:53:13.143996',
        'expires_at': '2017-03-08 22:53:13.143996'
    }
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(auth_object)
    }

