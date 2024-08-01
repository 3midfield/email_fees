from googleapiclient.discovery import build
import json
import pandas as pd
from bs4 import BeautifulSoup
import pinecone
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import WebBaseLoader

def split_docs(documents, chunk_size=750, chunk_overlap=20):
  print('nice')
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

import boto3
import boto3.dynamodb.conditions
from boto3.dynamodb.conditions import Key
import requests

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

# Use the function
data = check_for_repeat_company_name('Name', 'Company Name', 'Company Name', )
print(data)

def push_to_pinecone(csv_row):
    service = build('customsearch', 'v1', developerKey='AIzaSyCjvYaLI190wdKwqlq8vgXBqdMFKhEl_iU')
    pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
                environment='us-west4-gcp-free')

    model_name = 'text-embedding-ada-002'

    embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key='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'
    )
        
    name = csv_row["Company Name"]
    website = csv_row['Website']
    if name == check_for_repeat_company_name("us-east-2", 'AKIATHO4DCHKADOALXEX', 'wtAIEuZlZri61egkzw/NRjVJ4uvcq/c8YJL4Wvws', "Name", "Company Name", "Company Name", name):
        return "hi"
    else:
        res=(service.cse().list(q='about ' + name , cx="6064656ace39e41fc").execute())
        mission = (service.cse().list(q= name + ' mission' , cx="6064656ace39e41fc").execute())
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
            print(text)
            relevant_texts = relevant_texts + text
        for item in data2['items']:
            snippet = item['snippet']
            metatags = item.get('pagemap', {}).get('metatags', [])
            og_description = ''
            for metatag in metatags:
                og_description = metatag.get('og:description', '')
            soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
            text = soup.get_text()
            print(text)
            relevant_texts = relevant_texts + text
        print(relevant_texts)
        #This is my work to do Tres Frisard figure out how to upsert instead of pinecone.from_documents
        with open('parsing.txt', 'w') as f:
            f.write(relevant_texts)
        loader = TextLoader('parsing.txt')
        documents = loader.load() 
        docs = split_docs(documents)
        print(docs)
        index = Pinecone.from_documents(docs, embeddings, index_name="nice")
        push_company_name(name, "us-east-2", 'AKIATHO4DCHKADOALXEX', 'wtAIEuZlZri61egkzw/NRjVJ4uvcq/c8YJL4Wvws')