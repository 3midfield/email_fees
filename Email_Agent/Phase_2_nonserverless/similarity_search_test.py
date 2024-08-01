import os
import random
import sys
import csv
import pandas as pd
import pinecone
import openai
import numpy as np
from hubspot import push_to_hubspot

#from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import pandas as pd
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate


import openai


# Initialize the BERT model
model_name = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(
    model=model_name,
    openai_api_key='******************'
)
# Your query

pinecone.init(api_key='*****************',
              environment='us-west4-gcp-free')

#Iterate through all the people in the csv

emails_csv = pd.read_csv("/Users/") 
emails = emails_csv['Email Address']
list1 = emails_csv.loc[:, "Last Name"].values.tolist()
list2 = emails_csv.loc[:, "First Name"].values.tolist()
list3 = emails_csv.loc[:, "Company Name"].values.tolist()
list4 = []
list5 = []
background = "Background"

for i in range(len(list1)):
    list4.append(list1[i]+ " " + list2[i]) 
for i in range(len(list1)): 
    list5.append(list4[i]+ " " + list3[i])
for x in range(len(emails_csv)): #this is a test value right now of 10 to see if we can get 10 quality emails before we try it for the whole list
    # Call the API with your query
    llm = ChatOpenAI(model_name = 'gpt-3.5-turbo', openai_api_key='************************') 

    template = """  {background}, 
    and the context of the company to create this personalized email.
    {context}
    
    Memory: {memory}
    Human: {human_input}
    Chatbot:"""

    # prompt = PromptTemplate(
    #     input_variables=["human_input", "context"], template=template
    # )
    # conversation = LLMChain(
    # llm=llm,
    # prompt = prompt,
    # )
    # query = 'write an email that is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi to the first name of the person it is being sent to and an email sign off that has a line between it and the body saying best regards coming from Alexander Adams of no more than 3 sentences including: 1 subject line at the very beginning of the email titled Subject: , 1 sentence about how given recent announcements (product, partnerships, etc.) we assume they would want a 401(k) that integrates fully with their payroll  and 1 sentence that links to the 200+ payrolls with whom ForUsAll integrates https://www.forusall.com/payroll-partners using context and background information '
    # input_data = {"human_input": query, "context": context}

    # print(conversation.run({'human_input': "nice", 'context': "nice"}))

    prompt = PromptTemplate(

    input_variables=["background", "memory", "human_input", "context"],

    template=template,

    )
    memory = ConversationBufferMemory(memory_key="memory", input_key =  "human_input")
    chain = LLMChain(llm=llm, memory = memory, prompt=prompt)

    query = list5[x]
    # Vectorize the query
    query_vector = embeddings.embed_query(query)
    # print(np.shape(query_vector))
    index = pinecone.Index('nice')
    result = index.query(
        queries = [query_vector],
        top_k = 3,
        include_metadata = True# Number of similar items to retrieve
    )

    information = ""
    for i in range(3):
        information = information + result['results'][0]['matches'][i]['metadata']['text']
    #print(information)
    # print(result['results'])
    email_list = []
    # Replace 'your_api_key' with your actual API key
    openai.api_key = '***************'
    
    # The query you want to send
    query = 'Example'
                                      #ASK WHAT NAME WE WANT TO PROVIDE FOR THE BEST REGARDS PART #that has a line between it and the body
    # 1 Subject Line
    # 1 personalized sentence that is unique to their company to grab their attention that shows we researched the steam logistics website and that demonstrates we understand their company.  
    # 1 Sentence offering resources on different 401(k) providers.
    # 1 Question that elicits a reply from Steam Logistics."

    content = chain.run({

        'background': background,
        
        'human_input': query,
        
        'memory': memory,

        'context': information
        })
    
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + '\n' + str(emails[x])
    
    # Print the subject and body
    print(subject)
    print(body)
    email_list.append(subject)
    email_list.append(body)

    # Extract and print the response
#     email = llm([HumanMessage(content=query)])
#     #print(email)
#     content = conversation.predict(input=query)
#     split_content = content.split('\n', 1)
    
#     # Extract the subject and body
#     subject = split_content[0].replace('Subject: ', '')
#     body = split_content[1].strip() + '\n' + emails[x]
#     print(subject)
#     print(body)
#     # Print the subject and body
#     email_list.append(subject)
#     email_list.append(body)
    
    query = "Example"
    content = chain.run({

        'background': background,
        
        'human_input': query,
        
        'memory': memory,

        'context': information
        })
    
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + '\n' + str(emails[x])
    
    # Print the subject and body
    print(subject)
    print(body)
    email_list.append(subject)
    email_list.append(body)
#     email = llm([HumanMessage(content=query)])
#     #print(email)
#     content = conversation.predict(input=query)
#     split_content = content.split('\n', 1)
    
#     # Extract the subject and body
#     subject = split_content[0].replace('Subject: ', '')
#     body = split_content[1].strip() + '\n' + emails[x]
#     print(subject)
#     print(body)
#     # Print the subject and body
    
#     email_list.append(subject)
#     email_list.append(body)
    
    query = 'Example'
    content = chain.run({

        'background': background,
        
        'human_input': query,
        
        'memory': memory,

        'context': information
        })
    
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + '\n' + str(emails[x])
    
    # Print the subject and body
    print(subject)
    print(body)
    email_list.append(subject)
    email_list.append(body)
# email = llm([HumanMessage(content=query)])
#     #print(email)
#     content = conversation.predict(input=query)
#     split_content = content.split('\n', 1)
    
#     # Extract the subject and body
#     subject = split_content[0].replace('Subject: ', '')
#     body = split_content[1].strip() + '\n' + emails[x]
#     print(subject)
#     print(body)
#     # Print the subject and body
#     email_list.append(subject)
#     email_list.append(body)

    query = 'Example'
    content = chain.run({

        'background': background,
        
        'human_input': query,
        
        'memory': memory,

        'context': information
        })
    
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + '\n' + str(emails[x])
    
    # Print the subject and body
    print(subject)
    print(body)
    email_list.append(subject)
    email_list.append(body)