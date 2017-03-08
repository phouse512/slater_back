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

    # TODO: add validation that incoming attributes were sent correctly

    # TODO: add validation that password length is greater than 0
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

    storage_query = "INSERT INTO users (username, pw_hash, salt) values ('%s', '%s', '%s') returning id" % (
        incoming_object['username'], hashedpw, salt
    )

    cursor.execute(storage_query)
    new_user_id = cursor.fetchone()[0]
    connection.commit()

    create_bank_query = "INSERT INTO banks (entity_id, type, balance) values (%d, 'user', %d)" % (
        new_user_id, 270
    )
    cursor.execute(create_bank_query)
    connection.commit()

    return {
        'statusCode': 200,
        'headers': {},
        'body': ''
    }



