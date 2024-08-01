import json
import openai
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

def pinecone_push(event, context):
    # TODO implement
    print(event)
    csv_row = event['row']
    json_data = event['json_data']
    if 'body' in event:
        print(csv_row)
        pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
                    environment='us-west4-gcp-free')

        model_name = 'text-embedding-ada-002'

        embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key='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'
        )
        relevant_texts = event['body']
        with open('/tmp/parsing.txt', 'w') as f:
                f.write(relevant_texts)
        loader = TextLoader('/tmp/parsing.txt')
        documents = loader.load() 
        docs = split_docs(documents)
        print(docs)
        index = Pinecone.from_documents(docs, embeddings, index_name="nice")
        print('Yes it works')
    
    return {
        'statusCode': 200,
        'row' : csv_row,
        'json_data' : json_data
        }
