import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket = 'slater-storage'
    key = 'data/leaderboard.json'
    
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        json_data = data['Body'].read()
        
        return_object = {
            'statusCode': 200,
            'headers': {},
            'body': json_data
        }
        return return_object
    
    except Exception as e:
        print(e)
        raise e
 
