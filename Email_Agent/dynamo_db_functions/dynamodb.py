import boto3
import boto3.dynamodb.conditions
from boto3.dynamodb.conditions import Key
import requests

# #This is to add to the dynamodb
# "us-east-2"
# 'AKIATHO4DCHKADOALXEX'
# 'wtAIEuZlZri61egkzw/NRjVJ4uvcq/c8YJL4Wvws'
def push_company_name(company_name, region, key_id, secret_key):
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
    dynamoTable = dynamodb.Table("Name")
    dynamoTable.put_item(
        Item = {
            "Company Name": company_name
        }

    )

def push_accept_reject(company_name, region, key_id, secret_key):
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
    dynamoTable = dynamodb.Table("Name")
    dynamoTable.put_item(
        Item = {
            "Company Name": company_name
        }

    )

def check_for_repeat_company_name(region, key_id, secret_key, tableName, columnName, partitionKey, partitionKeyValue):
    dynamodb = boto3.resource(
        'dynamodb', region_name = region,
        aws_access_key_id= key_id,
        aws_secret_access_key= secret_key,
        )

    # Get the DynamoDB table
    table = dynamodb.Table(tableName)

    # Initialize an empty list to store column data
    column_data = []

    # DynamoDB Query operation
    response = table.query(
        KeyConditionExpression= Key(partitionKey).eq(partitionKeyValue)
    )

    for i in response['Items']:
        # Append each value in the column to the list
        if columnName in i:
            column_data.append(i[columnName])

    # If there are more items to be queried
    while 'LastEvaluatedKey' in response:
        response = table.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            KeyConditionExpression= Key(partitionKey).eq(partitionKeyValue)
        )
        
        for i in response['Items']:
            if columnName in i:
                column_data.append(i[columnName])

    return column_data

# Use the function
data = check_for_repeat_company_name("us-east-2", 'AKIATHO4DCHKADOALXEX', 'wtAIEuZlZri61egkzw/NRjVJ4uvcq/c8YJL4Wvws', 'Name', 'Company Name', 'Company Name', "nah")
print(data)