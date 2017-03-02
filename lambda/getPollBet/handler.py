import json


def lambda_handler(event, context):
    # TODO implement
    print(event)
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(event)
    }