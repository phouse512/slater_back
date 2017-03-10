import json
import boto3
import os
import psycopg2

s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    bucket = 'slater-storage'
    key = 'data/polls.json'

    user_id = int(event['requestContext']['authorizer']['principalId'])

    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    query = "select p.id, p.title, p.is_pre, p.close_time, p.buy_in, p.id, p.created_at, " \
            "json_agg(to_json(pa)) from polls p left join poll_answers pa on " \
            "pa.poll_id=p.id where p.finished=false and p.is_pre=false group by p.id"

    cursor.execute(query)
    results = cursor.fetchall()

    bets_query = "select p.id, count(b) from polls p left join bets b on p.id=b.poll_id where p.finished=false " \
                 "and p.is_pre=false group by p.id"
    cursor.execute(bets_query)
    bets = cursor.fetchall()

    bets_dict = dict()
    for bet in bets:
        bets_dict[bet[0]] = bet[1]

    user_bets_query = "select p.id from polls p left join bets b on p.id=b.poll_id where p.finished=false " \
                      "and p.is_pre=false and b.user_id=%d" % user_id
    cursor.execute(user_bets_query)
    personal_votes = cursor.fetchall()

    votes_dict = dict()
    for vote in personal_votes:
        votes_dict[vote[0]] = True

    print(votes_dict)

    connection.commit()
    polls = []

    for poll in results:
        json_blob = dict()
        json_blob['id'] = poll[0]
        json_blob['created'] = str(poll[6])
        json_blob['pre'] = str(poll[2]).lower()
        json_blob['current_votes'] = bets_dict[poll[0]]
        json_blob['answers'] = poll[7]
        json_blob['buy_in'] = poll[4]
        json_blob['question'] = poll[1]
        json_blob['close_time'] = str(poll[3])
        for answer in json_blob['answers']:
            answer['text'] = answer['title']
            answer.pop('title', None)
        print(poll[0])
        if poll[0] in personal_votes:
            print("ha")
            json_blob['voted'] = True
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
