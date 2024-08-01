import json
import boto3
from botocore.exceptions import ClientError

def send_email(event, context):
    ses = boto3.client('ses')
    print("It works!")
    sender_email = "alexander.adams@forusall.com" # Replace with your "From" email
    recipient_email = "andricosparis@gmail.com" # Replace with your "To" email
    aws_region = "us-east-1" # Replace with your AWS region

    subject = "Step Function Failure"
    body_text = "Step Function failed: " + json.dumps(event)

    try:
        response = ses.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [
                    recipient_email,
                ],
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    }
                }
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
