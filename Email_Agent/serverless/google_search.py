from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import json
import boto3
import boto3.dynamodb.conditions
from boto3.dynamodb.conditions import Key

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


def search(event, context):
    print(event)
    service = build('customsearch', 'v1', developerKey='AIzaSyDMuDfrL2bFwL6jfCK-Ugii20lEcn71Yhw')
    model_name = 'text-embedding-ada-002'
    csv_row = event['row']
    json_data = event['json_data']
    print(csv_row)
    name = csv_row['Company Name']
    print(name)
    name_list = [name]
    print(name_list)
    print(check_for_repeat_company_name("us-east-1", 'AKIAU75XLG6ZZU5LPIPA', 'E6wMgDBijh9btF/ZMrcAOHFYpmoz0WAXYL9/eOxR', "Name", "Company Name", "Company Name", name))
    if name_list == check_for_repeat_company_name("us-east-1", 'AKIAU75XLG6ZZU5LPIPA', 'E6wMgDBijh9btF/ZMrcAOHFYpmoz0WAXYL9/eOxR', "Name", "Company Name", "Company Name", name):
        return {
        'statusCode': 200,
        'row' : csv_row,
        'json_data' : json_data
        }

    else:
        res=(service.cse().list(q='about ' + name , cx="6064656ace39e41fc").execute())
        mission = (service.cse().list(q= name + ' mission' , cx="6064656ace39e41fc").execute())
        print(res)
        content = json.dumps(res) 
        data1 = json.loads(content)
        
        content2 = json.dumps(mission)
        data2=json.loads(content2)
        relevant_texts = ''

        for item in data1['items']:
            snippet = item['snippet']
            metatags = item.get('pagemap', {}).get('metatags', [])
            og_description = ''
            for metatag in metatags:
                og_description = metatag.get('og:description', '')
            soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
            text = soup.get_text()
            relevant_texts = relevant_texts + text
        for item in data2['items']:
            snippet = item['snippet']
            metatags = item.get('pagemap', {}).get('metatags', [])
            og_description = ''
            for metatag in metatags:
                og_description = metatag.get('og:description', '')
            soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
            text = soup.get_text()
            relevant_texts = relevant_texts + text
        push_company_name(name, "us-east-1", '', '')
     
        return {
            'statusCode': 200,
            'body': json.dumps(relevant_texts),
            'row' : csv_row,
            'json_data' : json_data
        }
