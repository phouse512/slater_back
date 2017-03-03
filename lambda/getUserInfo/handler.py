import json
import os
import psycopg2


def lambda_handler(event, context):
    # TODO implement
    connection = psycopg2.connect(database=os.environ['db'],
                                  user=os.environ['user'],
                                  password=os.environ['password'],
                                  host=os.environ['host'],
                                  port=os.environ['port'])
    cursor = connection.cursor()

    user_id = int(event['requestContext']['authorizer']['principalId'])

    """
        get winnings and put it in an array
    """

    """
        get bets made
    """
    bets_made_query = "select p.title, p.buy_in, pa.title from bets b left join polls p " \
                      "on p.id=b.poll_id left join poll_answers pa on p.id=pa.poll_id and pa.id=b.choice_id " \
                      "where p.finished=false and b.user_id=%d and p.has_paid=false" % user_id

    cursor.execute(bets_made_query)
    bets_made_results = cursor.fetchall()

    bets_made = []
    for made_bet in bets_made_results:
        obj = dict()
        obj['title'] = made_bet[0]
        obj['buy_in'] = made_bet[1]
        obj['choice'] = made_bet[2]
        bets_made.append(obj)

    """
        get closed bets
    """
    closed_bets_query = "select p.title, p.buy_in, pa.title from bets b left join polls p " \
                        "on p.id=b.poll_id left join poll_answers pa on p.id=pa.poll_id and pa.id=b.choice_id " \
                        "where p.finished=true and b.user_id=%d and p.has_paid=false" % user_id
    cursor.execute(closed_bets_query)
    closed_bets_results = cursor.fetchall()

    closed_bets = []
    for closed_bet in closed_bets_results:
        obj = dict()
        obj['title'] = closed_bet[0]
        obj['buy_in'] = closed_bet[1]
        obj['choice'] = closed_bet[2]
        closed_bets.append(obj)

    return_object = {
        'closed_bets': closed_bets,
        'open_bets': bets_made
    }

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(return_object)
    }
