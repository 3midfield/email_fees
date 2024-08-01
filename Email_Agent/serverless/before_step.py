import json
import csv
import boto3


def invoke(event, context):
    # TODO implement

    # Create a client
    client = boto3.client('stepfunctions')

    # Specify the ARN of your state machine
    state_machine_arn = 'arn:aws:states:us-east-1:343445026739:stateMachine:FullUnderscoreaiUnderscoreagentStepFunctionsStateMachine-vJkfuNkf7JGX'  # replace with your state machine ARN

    # Optionally, specify an input for the state machine
    input = json.dumps(event['Records'][0]['body'])  # replace with your input in JSON format, if any
    # Start an execution
    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=input
    )

    # Print the execution ARN
    print('Execution ARN:', response['executionArn'])
# import boto3

# # Create a client
# client = boto3.client('stepfunctions')

# # Specify the ARN of your state machine
# state_machine_arn = 'arn:aws:states:us-east-1:343445026739:stateMachine:FullUnderscoreaiUnderscoreagentStepFunctionsStateMachine-1YYqWVP4Yb5n'  # replace with your state machine ARN

# # Optionally, specify an input for the state machine
# input = json.dumps(event['Records'][0]['body'])  # replace with your input in JSON format, if any

# # Start an execution
# response = client.start_execution(
#     stateMachineArn=state_machine_arn,
#     input=input
# )

# # Print the execution ARN
# print('Execution ARN:', response['executionArn'])