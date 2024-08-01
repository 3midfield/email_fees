import pandas as pd
import pinecone
import csv
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone



def csv_pinecone():
    pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
                environment='us-west4-gcp-free')
    # pinecone.create_index("nice", dimension = 1536)
    model_name = 'text-embedding-ada-002'

    embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key='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'
    )
    loader = CSVLoader('with_email.csv')

    data = loader.load()


    index = Pinecone.from_documents(data, embeddings, index_name = "nice")
# Without Using A CSV Loader
# with open('with_email.csv') as csvfile:
#     csvreader = csv.reader(csvfile)
#     header = next(csvreader)
#     for row in csvreader:
#         print(row)
#         result.append(row)
# print(result[1])
# for i in range(1, len(result)):
#     index = Pinecone.from_texts(result[i], embeddings, index_name = "nice")


