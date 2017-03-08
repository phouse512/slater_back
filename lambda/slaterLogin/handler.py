import hashlib
import json
import os
import psycopg2
import uuid


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
    query = "SELECT id, username, created_at, pw_hash, salt from users WHERE username='%s' " \
            "LIMIT 1" % incoming_object["username"]
    cursor.execute(query)

    result = cursor.fetchone()

    if not result:
        return {
            'statusCode': 401,
            'headers': {},
            'body': ''
        }

    salt = result[4]
    hashed_input = hashlib.sha512(incoming_object['pw'] + salt).hexdigest()
    if hashed_input != result[3]:
        return {
            'statusCode': 403,
            'headers': {},
            'body': ''
        }

    # now logged in
    user_object = result
    auth_token_query = "SELECT id, user_id, auth_token FROM auth_tokens WHERE user_id=%d" % user_object[0]
    cursor.execute(auth_token_query)

    result = cursor.fetchone()
    if not result:
        auth_token = uuid.uuid4().hex
        create_auth_query = "INSERT INTO auth_tokens (user_id, auth_token) values (%d, '%s')" % (
            user_object[0], auth_token
        )

        cursor.execute(create_auth_query)
        connection.commit()

    else:
        auth_token = result[2]
        connection.commit()

    """
    insert device token into table on login
    """

    if 'device_token' in incoming_object:

        insert_token_query = "INSERT INTO device_tokens (user_id, token) values (%d, '%s')" % (
            user_object[0], incoming_object['device_token']
        )
        cursor.execute(insert_token_query)
        connection.commit()

    auth_object = {
        'auth_token': auth_token,
        'created_at': '2017-02-26 22:53:13.143996',
        'expires_at': '2017-03-08 22:53:13.143996'
    }
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(auth_object)
    }

