import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    
    bucket = 'slater-storage'
    key = 'data/confirm.json'
    
    print("deployed with cli")    
    
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

