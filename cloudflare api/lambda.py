import json
import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client
s3_client = boto3.client('s3')

# Replace with your actual bucket name and object key
BUCKET_NAME = 'phantom-vote-data'
FILE_NAME = 'passwords.json'

def lambda_handler(event, context):
    # Handle preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Use the correct domain in production
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'You can use POST to submit passwords'})
        }
    # Handle the GET request
    if event['httpMethod'] == 'GET':
        try:
            # Get the passwords data from S3
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
            passwords_data = json.loads(response['Body'].read().decode('utf-8'))
        except ClientError as e:
            print(f"Error getting object from S3: {e}")  # Log the error
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Error getting the passwords data'})
            }

        # Extract only the password-id and used status
        used_status_list = [{'password-id': pw['password-id'], 'used': pw['used']} for pw in passwords_data]

        # Respond with the password-ids and their used status
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(used_status_list)
        }
    # Handle the main POST request
    if event['httpMethod'] == 'POST':
        # Get the submitted password from the Lambda event
        try:
            submitted_password = json.loads(event['body'])['password']
        except (json.JSONDecodeError, KeyError):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': 'https://399.0236.fun, *'
                },
                'body': json.dumps({'error': 'Bad Request'})
            }

        # Get the passwords data from S3
        try:
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
            passwords_data = json.loads(response['Body'].read().decode('utf-8'))
        except ClientError as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)})
            }

        # Check if the submitted password (Unicode codepoints) is correct and not already used
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
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': str(e)})
                }
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'result': 'Success'})
            }
        else:
            return {
                'statusCode': 403,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'result': 'Error'})
            }
    else:
        # Method not allowed
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method Not Allowed'})
        }