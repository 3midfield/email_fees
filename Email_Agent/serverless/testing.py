from curses import keyname
from io import StringIO
import json
import csv
import boto3
import os

def nice(event, context):
    # Your function implementation here
    # implement boto to open the file and then parse through it(print the csv line as message payloads)
    # functional splitter
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/343445026739/myfirstqueue.fifo'
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    if not key.endswith('.csv'):
        print('File is not a CSV, exiting...')
        return {
            'statusCode': 200,
            'body': json.dumps('File is not a CSV')
        }
        
    print('Bucket name:', bucket_name)
    print('File name:', key)
    file_name = key.split('_')[1].split('.')[0]
    #file name should be everything after number and then the underscore
    file_name = file_name + '.json'
    
    
    try:
        data = s3.get_object(Bucket=bucket_name, Key=key)
        json_file = s3.get_object(Bucket=bucket_name, Key=file_name)
        
        csv_data = data['Body'].read().decode('utf-8')
        json_data = json_file['Body'].read().decode('utf-8')
        # Parse the CSV data
        csv_reader = csv.DictReader(StringIO(csv_data))
        
        rows = list(csv_reader)
        client = boto3.client('stepfunctions')

        # Specify the ARN of your state machine
        state_machine_arn = 'arn:aws:states:us-east-1:343445026739:stateMachine:FullUnderscoreaiUnderscoreagentStepFunctionsStateMachine-vJkfuNkf7JGX'  # replace with your state machine ARN
        # Optionally, specify an input for the state machine
        input = {
                'json_file': json_data,
                'csv': rows
                }  # replace with your input in JSON format, if any
        # Start an execution
        print(input)
        client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input)
        )

    except Exception as e:
        print(e)
        raise e
    print("Hello, world!")
    print('hello')
    return json.dumps(event)