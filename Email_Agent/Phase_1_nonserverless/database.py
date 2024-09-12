import os
import sys
import csv
import pandas as pd
import pinecone
import pprint
import json
import getpass
import random
import itertools
import numpy as np
from bs4 import BeautifulSoup
import fasttext
import tensorflow as tf
import openai

from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader, CSVLoader, WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma, Pinecone
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders.base import Document
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.utilities import ApifyWrapper
from googleapiclient.discovery import build


os.environ["APIFY_API_TOKEN"] = "***********************"
os.environ["OPENAI_API_KEY"] = "**************"
openai.api_key = "******************"

# PINECONE_ENV = getpass.getpass("us-west1-gcp")
# PINECONE_API_KEY = getpass.getpass("*********************")



# documents = ['experimenting.txt']


# # Create a dictionary from the list
# data_dict = {"sentences": data}

# Load the Universal Sentence Encoder's TF Hub module
# pinecone_index = pinecone.Index("nice")
# def text_to_vector(text):
#     """Convert a string of text into a FastText vector."""
#     # Preprocess the text
#     print(text)
#     sentence_vectors = model(text)
#     return sentence_vectors
    



# Assume your JSON data is a list of sentences under a "sentences" key
# sentences = data["sentences"]
# print(sentences)
# use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# # Convert a string to a vector representation

# vector = use_model(sentences)

# # Upsert the vectors and item IDs into the Pinecone index
# pinecone_index.upsert(ids=item_ids, vectors=vectors)


# TO LOAD IN THE CSV TO ADD TO PINECONE


# loader = CSVLoader(file_path='first_5.csv')
# data = loader.load()
# for data_id, embedding in data:
#     # Add the data to the Pinecone index
#     print(data_id)
#     print(embedding)
    # pinecone_index.upsert(ids=[data_id], vectors=[embedding])

#TO LOAD IN THE DIRECTORY TO PINECONE
pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
              environment='us-west4-gcp-free')

# pinecone.create_index("nice", dimension = 1536)
directory = '/Users/alexanderadams/ForUsAll-1/restructured'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents


documents = load_docs(directory)
print(documents)
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
print(docs)

model_name = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(
    model=model_name,
    openai_api_key='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'
)

#Add pinecone similiarity score
# index = Pinecone.from_documents(docs, embeddings, index_name="nice")
# index_description = pinecone.describe_index("nice")
# print(index_description)

# model_name = 'text-embedding-ada-002'

# embed = OpenAIEmbeddings(
#     model=model_name,
#     openai_api_key='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'
# )

# # index = pinecone.Index("nice")
# # print(pinecone.list_indexes)
# # response = index.query('', top_k = 5)
# # print(response)
# # vectorstore = Pinecone.from_existing_index(
# #     index, embed.embed_query, text_key= 'page_content'
# # )

# chain = RetrievalQA.from_chain_type(
#   llm=ChatOpenAI(openai_api_key='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', temperature=0.8, model="gpt-3.5-turbo", max_tokens=512),
#   chain_type="stuff",
# #   we must add the pinecone database
#   retriever=index.as_retriever()
# )
# responses = []
# with open('restructured/first_5.csv') as csv_file:
#     # this will be changed to the organized.csv(this is just for training)
#     dataframe = pd.read_csv(csv_file)
#     firsti = dataframe['First Name']
#     secondi = dataframe['Last Name']
#     company = dataframe['Company Name']
#     print(len(dataframe))
#     print(len(firsti))
#     for i in range(len(dataframe)):
#         print(firsti[i])
#         query =  (
#     "I will give you a question or an instruction. Your objective is to answer my question or : my instruction. My question or instruction is: Write a customized cold sales email cadence for "
#     + str(firsti[i]) + " " + str(secondi[i]) + " at " + str(company[i])
#     + ". The prospect is " + str(company[i])
#     + " has a 401(k) plan that had late payroll deposits on their last form 5500 filed with the IRS, which can create liability for the company and increases the chance of a DOL audit. Leverage information learned from the search results to make the email hyper relevant for this sales prospect. Each email should be concise and limited to 4 sentences at the most. Email 1 Outline:"
#     + "Opening sentence - provide a specific reason why we thought they would want to make sure their 401(k) is compliant based on what the company does, new products or their mission."
#     + "Sentence 2: Mention that we identified a late payroll deposit on their last 5500, and mention that this creates compliance risk."
#     + "Sentence 3: start a new paragraph. Acknowledge that the CEO is probably not handling payroll, but that we have tools their team can use to integrate the 401(k) with payroll to help eliminate late payrolls."
#     + "Sentence 4: start a new paragraph. Ask who on their team we should followup with."
#     + "Email 2 Outline:"
#     + "Opening sentence -Acknowledge that the CEO is probably focusing on [mention any specific new products, new executive hires, or business priorities] not handling payroll, but late payrolls are creating a compliance risk that could derail their primary business goals."
#     + "Sentence 2: Provide a link to https://www.forusall.com/payroll-partners to learn more about integrating payroll with the 401(k)"
#     + "Sentence 3: Ask who on their team we should followup with."
#     + "Email 3:"
#     + " Sentence 1: Acknowledge that growing the company [mention any new products and/or services] is probably the focus and that ensuring timely payroll deposits into the 401k is likely lowest on the priority list."
#     + "Sentence 2: new paragraph. Mention that new payroll integrations can be setup in minutes - saving the team hours of work each payroll cycle."
#     + "Sentence 3: new paragraph Link to this blogpost. www.forusall.com which highlights the risks of not having payroll integrated."
#     + "For your reference, todays date is June 27, 2023.")
# #         responses.append(chain.run(query))
# # print(responses) 

#         # add the actual message we want to query with the four different emails
#         print(chain.run(query))
        
        
# # Create an empty list to store the responses

# # Generate and store the responses
# # for i in range(len(dataframe)):
# #     response = openai.Completion.create(engine='text-davinci-003',
# #         prompt=query,
# #         max_tokens=50,
# #         n=1,
# #         stop=None
# #     )
# # responses.append(chain.run(query))
# # print(responses)

# # Print the stored responses
# # for response in responses:
# #     print(responses)

#         # NEED THE HUBSPOT API KEY TO THEN SEND THE [chain.run(query)] to Hubspot



# # def encode_text(text):
# #     return embed([text]).numpy()[0]

# # file_path = 'experimenting.txt'  # Replace with the actual file path
# # with open(file_path, 'r') as file:
# #     file_contents = file.read()
    
# # file_vector = encode_text(file_contents)

# # pinecone_index.upsert([file_vector])

#     # Extract relevant text from file


# #     # Use your text embedding model to convert the text into a vector
# #     print(text)
# #     words = text.split()  # Split the text into individual words
# #     vector = np.mean([model.wv[word] for word in words if word in model.wv], axis=0)
# #     return vector

# # for file_path, content in loader.load():
# #     # Assuming each file contains a single text document
# #     vector = text_to_vector(content)
# #     pinecone_index.upsert(ids=file_path, vectors=[vector])

# # def map_fn(item):
# #     # Convert item to a Pinecone Vector object
# #     values = pd.Series([1.0, 2.0, 3.0])
# #     vector = pinecone.Vector(values)
# #     return vector
# # # docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# # embedding = np.array([0.1, 0.2, 0.3])
# # item_id = 'item123'
# # pinecone_index.upsert(ids=[item_id], vectors=[embedding])
# # def chunks(iterable, batch_size=100):
# #     """A helper function to break an iterable into chunks of size batch_size."""
# #     it = iter(iterable)
# #     chunk = tuple(itertools.islice(it, batch_size))
# #     while chunk:
# #         yield chunk
# #         chunk = tuple(itertools.islice(it, batch_size))

# # vector_dim = 128
# # vector_count = 1000

# # # # # # Ensure that each item can be properly serialized
# # # # # list_of_serializable_items = []

# # # # # for item in docs:
# # # # #     print(item)
# # # #     serialized_item = map_fn(item)
# # # #     list_of_serializable_items.append(serialized_item)
# # # # # Example generator that generates many (id, vector) pairs
# files_generator = map(lambda i: (f'id-{i}', vector), range(vector_count))



# for ids_vectors_chunk in chunks(files_generator, batch_size=100):
#     print('nice')
#     pinecone_index.upsert(vectors=ids_vectors_chunk)

# # Example generator that generates many (id, vector) pairs
# example_data_generator = map(lambda i: (f'id-{i}', [random.random() for _ in range(128)]), range(10000))
