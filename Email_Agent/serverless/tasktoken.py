import boto3
import json

def start_step(event, context):
    sfn = boto3.client('stepfunctions')
    print(event)
    token = event['queryStringParameters']['token']    # get the token from the query string
    please = token.replace(' ', '+')
    print(please)
    if event['resource'] == '/accept':
        key = {'testing': 'emaildata',
        }
        dynamodb = boto3.resource('dynamodb')

        # Get the table
        table = dynamodb.Table('table-one')
        response = table.get_item(Key=key)
        item = response.get('Item')
        print(item)
        response = sfn.send_task_success(
            taskToken= please,
            output= json.dumps(item)
        )
        delete_key = table.delete_item(Key=key)

        # Print the response
        print(delete_key)
    else:
        key = {'testing': 'emaildata',
        }
        dynamodb = boto3.resource('dynamodb')

        # Get the table
        table = dynamodb.Table('table-one')
        delete_key = table.delete_item(Key=key)
        response = sfn.send_task_failure(
            cause='The operation was rejected by the user',
            error='OperationRejected',
            taskToken= please,
        )
        print(delete_key)
    print(response)
    return {
        'statusCode': 200,
        'body': 'Operation approved successfully'
    }