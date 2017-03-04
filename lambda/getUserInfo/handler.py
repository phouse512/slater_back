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
    get user's bank id
    """
    get_user_bank_id = "select id from banks where entity_id=%d and type='user' limit 1" % user_id
    cursor.execute(get_user_bank_id)
    user_bank_id = cursor.fetchone()[0]

    if not user_bank_id:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'error': 'user has no bank account'})
        }

    """
        get winnings and put it in an array
    """
    winnings = []
    get_recently_paid_out_polls = "select p.title, b.id, ba.id from bets b left join polls p " \
                                  "on p.id=b.poll_id left join banks ba on ba.entity_id=p.id and " \
                                  "ba.type='poll' where b.user_id=%d and has_paid=true" % user_id

    cursor.execute(get_recently_paid_out_polls)
    paid_out_bets = cursor.fetchall()

    for bet in paid_out_bets:
        poll_bank_id = bet[2]
        paid_bets_query = "select id, balance, type from transactions where (from_entity=%d and " \
                          "to_entity=%d and type='bet') or (from_entity=%d and to_entity=%d and " \
                          "type='payout')" % (user_bank_id, poll_bank_id, poll_bank_id, user_bank_id)

        cursor.execute(paid_bets_query)
        transactions = cursor.fetchall()
        sum = 0
        for transaction in transactions:
            if transaction[2] == 'bet':
                sum -= transaction[1]
            else:
                sum += transaction[1]

        winnings.append({
            'title': bet[0],
            'winnings': sum
        })

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
        'open_bets': bets_made,
        'winnings': winnings
    }

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(return_object)
    }
