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

    query = "SELECT id, username, created_at, pw_hash from users WHERE username='%s' " \
            "LIMIT 1" % incoming_object["username"]
    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'error': 'User already exists'})
        }

    salt = uuid.uuid4().hex
    hashedpw = hashlib.sha512(incoming_object['pw'] + salt).hexdigest()

    storage_query = "INSERT INTO users (username, pw_hash, salt) values (%s, %s, %s)" % (
        incoming_object['username'], hashedpw, salt
    )

    cursor.execute(storage_query)
    connection.commit()

    return {
        'statusCode': 200,
        'headers': {},
        'body': ''
    }



