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

search_list = []
service = build('customsearch', 'v1', developerKey='')
pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
            environment='us-west4-gcp-free')

model_name = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(
    model=model_name,
    openai_api_key='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'
)


def split_docs(documents, chunk_size=750, chunk_overlap=20):
  print('nice')
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

with open('/Users/alexanderadams/ForUsAll-1/AI Agent List - July_21.csv') as csv_file:
# should be organized.csv when actually running(this is just for training)
    #THIS IS TO UPLOAD THE CSV FILE
    loader = CSVLoader('/Users/alexanderadams/ForUsAll-1/AI Agent List - July_21.csv')
    data = loader.load()
    index = Pinecone.from_documents(data, embeddings, index_name = "nice")
    
    
    dataframe = pd.read_csv(csv_file)
    name = dataframe['Company Name']
    website = dataframe['Website']
    for i in range(len(dataframe)):
        # if index.namespace == name[i]:
        #     print("already in pinecone")
    # else:    
        if name[i] in search_list:
            print('found in list')
        else:
            search_list.append(name[i])
            res=(service.cse().list(q='about ' + name[i] , cx="6064656ace39e41fc").execute())
            mission = (service.cse().list(q= name[i] + ' mission' , cx="6064656ace39e41fc").execute())
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
            # print(text)
            relevant_texts = relevant_texts + text
        for item in data2['items']:
            snippet = item['snippet']
            metatags = item.get('pagemap', {}).get('metatags', [])
            og_description = ''
            for metatag in metatags:
                og_description = metatag.get('og:description', '')
            soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
            text = soup.get_text()
            # print(text)
            relevant_texts = relevant_texts + text
        # print(relevant_texts)
        with open('parsing.txt', 'w') as f:
            f.write(relevant_texts)
        loader = TextLoader('parsing.txt')
        documents = loader.load() 
        docs = split_docs(documents)
        index = Pinecone.from_documents(docs, embeddings, index_name="nice")
