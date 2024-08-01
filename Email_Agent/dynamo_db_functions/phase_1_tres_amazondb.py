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
import typing

import boto3
import boto3.dynamodb.conditions as conditions
import requests

client = boto3.client(
    'dynamodb', region_name = "us-east-2",
    aws_access_key_id='AKIATHO4DCHKADOALXEX',
    aws_secret_access_key='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',
    )
dynamodb = boto3.resource(
    'dynamodb', region_name = "us-east-2",
    aws_access_key_id='AKIATHO4DCHKADOALXEX',
    aws_secret_access_key='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',
    )
ddb_exceptions = client.exceptions
dynamoTable = dynamodb.Table("Name")
string = "Hello"
dynamoTable.put_item(
    Item = {
        "Company Name": string,
    }

)


# search_list = []
# service = build('customsearch', 'v1', developerKey='AIzaSyCjvYaLI190wdKwqlq8vgXBqdMFKhEl_iU')
# pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
#             environment='us-west4-gcp-free')

# model_name = 'text-embedding-ada-002'

# embeddings = OpenAIEmbeddings(
#     model=model_name,
#     openai_api_key='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'
# )


# def split_docs(documents, chunk_size=750, chunk_overlap=20):
#   print('nice')
#   text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#   docs = text_splitter.split_documents(documents)
#   return docs

# # with open('/Users/kennethfrisardiii/Downloads/ForUsAll/test_run.csv') as csv_file:
# # should be organized.csv when actually running(this is just for training)
#     #THIS IS TO UPLOAD THE CSV FILE
#     # loader = CSVLoader('/Users/kennethfrisardiii/Downloads/ForUsAll/test_run.csv')
#     # data = loader.load()
#     # index = Pinecone.from_documents(data, embeddings, index_name = "nice")
    
    
# # dataframe = pd.read_csv(csv_file)
# # name = dataframe['Company Name']
# # website = dataframe['Website']
# # for i in range(len(dataframe)):
# # # if :
# # #     print("already in pinecone")
# # # else:    

# # create a client for S3 service
# s3_client = boto3.client('s3', region_name='us-west-2')

# client = boto3.client(
#     's3',  region_name = 'us-west-2',
#     aws_access_key_id='YOUR_ACCESS_KEY',
#     aws_secret_access_key='YOUR_SECRET_KEY',
#     aws_session_token='YOUR_SESSION_TOKEN',  # optional
# )

# # create a resource for DynamoDB
# dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

# # Specify the table
# table = dynamodb.Table('Names')  # replace with your table name

# # Specify the primary key of the item
# key = {'Company Name': 'String'}  # replace with your primary key

# # Specify the new value to add to the list
# new_value = 'Hi'  # replace with your new value

# # Update the item
# response = table.update_item(
#     Key=key,
#     UpdateExpression='SET your-list-attribute = list_append(if_not_exists(your-list-attribute, :empty_list), :new_value)',
#     ExpressionAttributeValues={
#         ':new_value': [new_value],
#         ':empty_list': []
#     },
#     ReturnValues='UPDATED_NEW'
# )

# # Print the updated list
# print(response['Attributes']['your-list-attribute'])

# def append_measurement_to_sensor(sensor_id: str, measurement: int, TABLE_NAME):
#     """Add a measurement to a sensor if said sensor exists"""

#     table = boto3.resource("dynamodb").Table(TABLE_NAME)

#     try:
#         table.update_item(
#             Key={
#                 "PK": f"S#{sensor_id}",
#             },
#             UpdateExpression="SET #m = list_append(#m, :measurement)",
#             ExpressionAttributeNames={
#                 "#m": "measurements",
#             },
#             ExpressionAttributeValues={
#                 ":measurement": [measurement]
#             },
#             ConditionExpression=conditions.Attr("PK").exists()

#         )
#     except ClientError as err:
#         if err.response["Error"]["Code"] == 'ConditionalCheckFailedException':
#             raise ValueError("Sensor doesn't exist") from err
#         else:
#             raise err

# def push_to_pinecone(name):
#     if name in #global variable:
#         print('found in list')
#     else:
#         search_list.append(name) #append to global variable
#         res=(service.cse().list(q='about ' + name , cx="6064656ace39e41fc").execute())
#         mission = (service.cse().list(q= name + ' mission' , cx="6064656ace39e41fc").execute())
#     content = json.dumps(res) 
#     data1 = json.loads(content)

#     content2 = json.dumps(mission)
#     data2=json.loads(content2)
#     relevant_texts = ''

#     for item in data1['items']:
#         snippet = item['snippet']
#         metatags = item.get('pagemap', {}).get('metatags', [])
#         og_description = ''
#         for metatag in metatags:
#             og_description = metatag.get('og:description', '')
#         soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
#         text = soup.get_text()
#         # print(text)
#         relevant_texts = relevant_texts + text
#     for item in data2['items']:
#         snippet = item['snippet']
#         metatags = item.get('pagemap', {}).get('metatags', [])
#         og_description = ''
#         for metatag in metatags:
#             og_description = metatag.get('og:description', '')
#         soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
#         text = soup.get_text()
#         # print(text)
#         relevant_texts = relevant_texts + text
#     # print(relevant_texts)
#     with open('parsing.txt', 'w') as f:
#         f.write(relevant_texts)
#     loader = TextLoader('parsing.txt')
#     documents = loader.load() 
#     docs = split_docs(documents)
#     # print(docs)
#     the_namespace = name[i]
#     index = Pinecone.from_documents(docs, embeddings, index_name="nice", namespace = the_namespace)
    
# print(index.query("nice"))
# print(f"Index {"nice"} exists with namespace {info['namespace']}") namespace {info['namespace']}") except pinecone.exceptions.PineconeException:print(f"Index {index_name} does not exist")


# print(documents)


# docs = split_docs(documents)
# print(docs)
# def pine(docs):
#     index = Pinecone.from_documents(docs, embeddings, index_name="nice")
#     index_description = pinecone.describe_index("nice")
#     print(index_description)
    
# pine(docs)