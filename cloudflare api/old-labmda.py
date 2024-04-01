import json
import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client
s3_client = boto3.client('s3')

# Replace with your actual bucket name and object key
BUCKET_NAME = 'phantom-vote-data'
FILE_NAME = 'passwords.json'

def lambda_handler(event, context):
    # Get the submitted password from the Lambda event
    try:
        submitted_password = json.loads(event['body'])['password']
    except (json.JSONDecodeError, KeyError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Bad Request'})
        }

    # Get the passwords data from S3
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        passwords_data = json.loads(response['Body'].read().decode('utf-8'))
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    # Check if the submitted password is correct and not already used
    password_match = False
    for password_entry in passwords_data:
        if password_entry['password'] == submitted_password and password_entry['used'] == 0:
            password_match = True
            password_entry['used'] = 1  # Mark as used
            break

    # Update the passwords file in S3 if there was a match
    if password_match:
        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=FILE_NAME, Body=json.dumps(passwords_data))
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
        return {
            'statusCode': 200,
            'body': json.dumps({'result': 'Success'})
        }
    else:
        return {
            'statusCode': 403,
            'body': json.dumps({'result': 'Error'})
        }
