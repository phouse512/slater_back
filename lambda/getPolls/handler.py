import json
import boto3
import os
import psycopg2

s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    bucket = 'slater-storage'
    key = 'data/polls.json'

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    query = "select p.id, p.title, p.is_pre, p.close_time, p.buy_in, p.id, p.created_at," \
            " json_agg(to_json(pa)) from polls p " \
            "left join poll_answers pa on pa.poll_id=p.id group by p.id"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.commit()
    polls = []

    for poll in results:
        json_blob = dict()
        json_blob['id'] = poll[0]
        json_blob['created'] = str(poll[6])
        json_blob['pre'] = str(poll[2]).lower()
        json_blob['current_votes'] = 23
        json_blob['answers'] = poll[7]
        json_blob['buy_in'] = poll[4]
        json_blob['question'] = poll[1]
        json_blob['close_time'] = str(poll[3])
        for answer in json_blob['answers']:
            answer['text'] = answer['title']
            answer.pop('title', None)
        polls.append(json_blob)

    return_object = {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(polls)
    }

    return return_object

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
