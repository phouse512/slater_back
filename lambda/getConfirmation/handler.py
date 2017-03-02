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

    user_id = event['requestContext']['authorizer']['principalId']
    poll_id = event['pathParameters']['poll_id']

    incoming_object = json.loads(event['body'])
    answer_id = incoming_object['answer_id']

    
    # bucket = 'slater-storage'
    # key = 'data/confirm.json'
    #
    # print("deployed with cli")
    #
    # try:
    #     data = s3.get_object(Bucket=bucket, Key=key)
    #     json_data = data['Body'].read()
    #
    #     return_object = {
    #         'statusCode': 200,
    #         'headers': {},
    #         'body': json_data
    #     }
    #     return return_object
    #
    # except Exception as e:
    #     print(e)
    #     raise e
    #
