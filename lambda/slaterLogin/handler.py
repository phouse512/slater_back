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

    print(event)
    print(connection)

    auth_object = {
        'auth_token': 'fictional-auth-token',
        'created_at': '2017-02-26 22:53:13.143996',
        'expires_at': '2017-03-08 22:53:13.143996'
    }
    
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(auth_object)
    }

