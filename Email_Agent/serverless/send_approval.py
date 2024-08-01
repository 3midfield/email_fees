import boto3
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def add_data(data, region, key_id, secret_key):
    client = boto3.client(
        'dynamodb', region_name = region,
        aws_access_key_id= key_id,
        aws_secret_access_key= secret_key,
        )
    dynamodb = boto3.resource(
        'dynamodb', region_name = region,
        aws_access_key_id= key_id,
        aws_secret_access_key= secret_key,
        )
    ddb_exceptions = client.exceptions
    dynamoTable = dynamodb.Table("table-one")
    dynamoTable.put_item(
        Item = {
            "testing": "emaildata",
            "data": data
        }

    )

def send_email(event, context):
    add_data(event['input'], "us-east-1", 'AKIAU75XLG6ZZU5LPIPA', 'E6wMgDBijh9btF/ZMrcAOHFYpmoz0WAXYL9/eOxR')
    print(event)
    token = event['token']
    email_body = []
    email_names = []
    sns = boto3.client('sns')
    client = boto3.client('ses',region_name="us-east-1")
    print(event)
    for i in range(len(event)):
        email_names.append("<b>" + event['input'][i]['row']['First Name'] + " " + event['input'][i]['row']['Last Name'] + "</b>")
        email_body.append(event['input'][i]['email'])
    #we are using email-data-api for api gateway 
    formatted_strings = [f"{name}: {emails}" for name, emails in zip(email_names, email_body)]
    message = "<br><br>".join(formatted_strings)
    approval_url = f"https://94lb31v4j1.execute-api.us-east-1.amazonaws.com/dev/accept?token={token}"
    message = message + f'<br><br>To accept this message, click this url: <a href="{approval_url}">Accept here</a>'
    
    reject_url = f"https://94lb31v4j1.execute-api.us-east-1.amazonaws.com/dev/reject?token={token}"
    message = message + f'<br><br>To reject this message, click this url: <a href="{reject_url}">Reject here</a>'
    print(message)
    
    
    # response = sns.publish(
    #     TopicArn='arn:aws:sns:us-east-1:343445026739:emailmarketing',    # replace with your SNS Topic ARN
    #     Message= message,    # replace with your message and URLs
    #     Subject='Outbound Marketing Emails' 
    # )
    
    #Official Email to use when running the program: andricosparis@gmail.com
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    'andricosparis@gmail.com',
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': message,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Outbound Marketing Emails',
                },
            },
            Source='alexander.adams@forusall.com',
        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


    return event