from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import pandas as pd
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
# THIS CODE HAS NOT BEEN RAN YET
# pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
#               environment='us-west4-gcp-free')
# model_name = 'text-embedding-ada-002'

# embed = OpenAIEmbeddings(
#     model=model_name,
#     openai_api_key='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'
# )

# index = pinecone.Index("nice")


# llm=ChatOpenAI(openai_api_key='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', temperature=0.8, model="gpt-3.5-turbo", max_tokens=512),
  

# query = 'write an email to Silva Ricardo using this information:'
                    
# with open('first_5.csv') as csv_file:
#     # this will be changed to the organized.csv(this is just for training)
#     dataframe = pd.read_csv(csv_file)
#     firsti = dataframe['First Name']
#     secondi = dataframe['Last Name']
#     print(len(dataframe))
#     print(len(firsti))
#     for i in range(len(dataframe)):
#         print(firsti[i])
#         query = 'write an email marketing ForUsAll to ' + firsti[i] + ' ' + secondi[i]
#         # add the actual message we want to query with the four different emails
#         print(query)
#         print(llm(query))
#         # NEED THE HUBSPOT API KEY TO THEN SEND THE [chain.run(query)] to Hubspot


