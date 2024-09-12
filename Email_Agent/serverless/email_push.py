import json
import pinecone
import openai
import requests
# from sendgrid import push_to_sendgrid

#from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# def push_to_hubspot(email_list, dataframe):
#     company = dataframe['Company Name']
#     website = dataframe['Website']
#     first_name = dataframe['First Name']
#     last_name = dataframe['Last Name']
#     email = dataframe['Email Address']

    
#     address = dataframe['Full Address']
#     job_title = dataframe["Job Title"]
#     phone_number = dataframe["Direct Phone Number"]
#     mobile_number = dataframe["Mobile phone"]
#     zoom_info_contact = dataframe["ZoomInfo Contact Profile URL"]
#     linkedin_contact = dataframe["LinkedIn Contact Profile URL"]
#     revenue = dataframe["Revenue (in 000s USD)"]
#     employees = dataframe["Employees"]
#     zoom_info_company = dataframe["ZoomInfo Company Profile URL"]
#     linkedin_company = dataframe["LinkedIn Company Profile URL"]
#     department = dataframe["Department"]
#     access_token = '*************'
#     headers = {
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             'Authorization': f'Bearer {access_token}'
#         }
#     data = {
#         "fields": [
#         {
#         "objectTypeId": "0-1",
#         "name": "lastname",
#         "value": str(last_name)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "firstname",
#         "value": str(first_name)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "jobtitle",
#         "value": str(job_title)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "direct_phone",
#         "value": str(phone_number)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "email",
#         "value": str(email)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "department",
#         "value": str(department)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "mobilephone",
#         "value": str(mobile_number)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "zoominfo_contact_profile_url",
#         "value": str(zoom_info_contact)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "person_linkedin_url__c",
#         "value": str(linkedin_contact)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "company",
#         "value": str(company)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "website",
#         "value": str(website)
#         },
#         {
#         "objectTypeId": "0-2",
#         "name": "company_revenues",
#         "value": str(revenue)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "company_size",
#         "value": str(employees)
#         },
#         {
#         "objectTypeId": "0-2",
#         "name": "zoominfo_company_profile_url",
#         "value": str(zoom_info_company)
#         },
#         {
#         "objectTypeId": "0-2",
#         "name": "company_linkedin_url__c",
#         "value": str(linkedin_company)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "address",
#         "value": str(address)
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "subject_1",
#         "value": str(email_list[0])
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "email_body_1",
#         "value": email_list[1]
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "subject_2",
#         "value": str(email_list[2])
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "email_body_2",
#         "value": email_list[3]
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "subject_3",
#         "value": str(email_list[4])
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "email_body_3",
#         "value": email_list[5]
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "subject_4",
#         "value": str(email_list[6])
#         },
#         {
#         "objectTypeId": "0-1",
#         "name": "email_body_4",
#         "value": email_list[7]
#         }]
#     }
#     return data
#     # submission = requests.post('https://api.hsforms.com/submissions/v3/integration/submit/5352904/24ed8f28-e0e0-4160-b599-cae31e8880b4', headers=headers, data = json.dumps(data))
#     # print(submission)

def hubspot(event, context):
    # TODO implement
    print(event)
    # Initialize the BERT model
    dict_data = event['row']
    json_string = event['json_data']
    json_data = json.loads(json_string)
    print(json_data)
    first_name = dict_data['First Name']
    print(first_name)
    last_name = dict_data['Last Name']
    company_name = dict_data['Company Name']
    
    
    model_name = 'text-embedding-ada-002'

    embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key='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'
    )
    # Your query
    query = first_name + ' ' + last_name + ' ' + company_name
    pinecone.init(api_key='2af041ae-aeae-4970-92ef-123f57f551c8',
                environment='us-west4-gcp-free')

    #Iterate through all the people in the csv

    
    background = "Background on ForUsAll: ForUsAll has two core products, a full-service 401(k) platform (ForUsAll 401(k)) and Advisor+ Full-service 401(k) platform A turnkey 401(k) platform that provides everything you need to setup a  401(k) employees rave about.Best for: Companies setting up a new 401(k) - or replacing an old one. * Unmatched investment choice = more opportunities for growth * Payroll integration = save time * Automated administration = save time, reduce errors * Financial advisor for employees = higher savings rates3 * Fiduciary protection = reduce your liability * Recordkeeping Advisor+ Easily modernize and automate your existing 401(k) without changing providers. Best for: Companies looking to upgrade their current 401(k) while lowering costs. * Works with your existing provider = easy to upgrade * Payroll integration = save time * Automated administration = save time, reduce errors * Financial advisors for employees = higher savings rates3 * Fiduciary protection = reduce your liability  With the new Secure Act 2.0, tax credits may cover up to 100% of employer costs for the first 3 years.  Please make sure that the emails do not violate any of the SEC marketing rules - no promissory language and no rocket emojis."

    
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
    
    print(information)
    #print(information)
    # print(result['results'])
    email_list = []
    # Replace 'your_api_key' with your actual API key
    openai.api_key = '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'
    
    # The query you want to send
    # query = 'write an email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi ' + first_name + ' and an email sign off saying Best Regards coming from Drew Miller of no more than 4 sentences, including: 1 subject line at the very beginning of the email titled Subject: , 1 personalized sentence that is unique to their company to grab their attention that shows we researched their company and that ties their company mission to offering a great 401(k), 1 Sentence offering a 401(k) shopping guide that can help them quickly evaluate top 401k providers, and 1 Question that elicits a reply using this information: ' + information + background
    query = 'write an email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi ' + first_name + ' and an email sign off saying Best Regards coming from Drew Miller of no more than ' + json_data['query1'] + ': ' + information + background
                                    #ASK WHAT NAME WE WANT TO PROVIDE FOR THE BEST REGARDS PART #that has a line between it and the body
    # 1 Subject Line
    # 1 personalized sentence that is unique to their company to grab their attention that shows we researched the steam logistics website and that demonstrates we understand their company.  
    # 1 Sentence offering resources on different 401(k) providers.
    # 1 Question that elicits a reply from Steam Logistics."

    # Call the API with your query
    llm = ChatOpenAI(model_name = 'gpt-4', openai_api_key='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')
    # Extract and print the response
    email = llm([HumanMessage(content=query)])
    #print(email)
    content = email.content
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + " "
    
    # Print the subject and body
    email_list.append(subject)
    email_list.append(body)
    
    # query = 'write an email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi ' + first_name + ' and an email sign off that has a line between it and the body saying Best Regards coming from Drew Miller of no more than 3 sentences including: 1 subject line at the very beginning of the email titled Subject: , 1 sentence about how given recent announcements (product, partnerships, etc.) we assume they would want a 401(k) that integrates fully with their payroll  and 1 sentence that links to the 200+ payrolls with whom ForUsAll integrates https://www.forusall.com/payroll-partners using this information: ' + information + background
    
    query = 'write an email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi ' + first_name + ' and an email sign off that has a line between it and the body saying Best Regards coming from Drew Miller of no more than ' + json_data['query2'] + ': ' + information + background
    
    email = llm([HumanMessage(content=query)])
    #print(email)
    content = email.content
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + ' '

    # Print the subject and body
    email_list.append(subject)
    email_list.append(body)
    
    # query = 'write an email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi ' + first_name + ' and an email sign off that has a line between it and the body saying Best Regards coming coming from Drew Miller of no more than 3 sentences including: 1 subject line at the very beginning of the email titled Subject: , 1 sentence about Secure Act 2.0 making it easier than ever for budget-conscious companies to offer a 401(k), and 1 sentence contractor team arrangement to the Secure Act ForUsAll calculator https://www.forusall.com/secureact-tax-credit which allows users to calculate tax-credits that may cover up to 100 percent of employer 401(k) costs in the first few years using this information: ' + information + background
    
    query = 'write an email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation saying Hi ' + first_name + ' and an email sign off that has a line between it and the body saying Best Regards coming coming from Drew Miller of no more than ' + json_data['query3'] + ': ' + information + background
    email = llm([HumanMessage(content=query)])
    #print(email)
    content = email.content
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + ' '

    # Print the subject and body
    email_list.append(subject)
    email_list.append(body)

    # query = 'write a breakup email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation only saying the word Hi ' + first_name + ' and an email sign off that has a line between it and the body saying Best Regards coming from Drew Miller of no more than 4 sentences including: 1 subject line at the very beginning of the email titled Subject: , 1 sentence about a recent event the company had and why I thought they would want an automated 401(k).  Confirm that either 1) they aren’t interested in upgrading a 401(k) or if: 2) the timing might not be right using this information: ' + information + background
    
    query = 'write a breakup email that has no underscores or dashes and is casual, concise and written to an 8th grade reading level that includes a salutation only saying the word Hi ' + first_name + ' and an email sign off that has a line between it and the body saying Best Regards coming from Drew Miller of no more than ' + json_data['query4'] + ': ' + information + background
    
    email = llm([HumanMessage(content=query)])
    #print(email)
    content = email.content
    split_content = content.split('\n', 1)
    
    # Extract the subject and body
    subject = split_content[0].replace('Subject: ', '')
    body = split_content[1].strip() + ' '

    # Print the subject and body
    email_list.append(subject)
    email_list.append(body)


    email_list = [sub.replace('\n\n', '\n \n') for sub in email_list]
    email_list = [sub.replace('Best Regards,\n', 'Best Regards,') for sub in email_list] 
    email_list = [sub.replace('Best Regards,\n \n', 'Best Regards,') for sub in email_list]
    email_list = [sub.replace('Best Regards, \n \n', 'Best Regards,') for sub in email_list]
    email_list = [sub.replace('Best Regards, \n \n', 'Best Regards,') for sub in email_list]
    email_list = [sub.replace(' Best Regards,', 'Best Regards,') for sub in email_list]
    email_list = [sub.replace('Drew Miller', '') for sub in email_list]
    email_list = [sub.replace('Best Regards,', '') for sub in email_list]
    # email_list= [sub.replace('Drew Miller', ' <strong> Drew Miller </strong> ') for sub in email_list]
    # email_list= [sub.replace('Hi', 'Hi ' + first_name) for sub in email_list]
    
    #THE LINE BENEATH IS HOW WE ADD EVERYTHING TO HUBSPOT WITH ONE PUSH
    # data = push_to_hubspot(email_list=email_list, dataframe = dict_data)
    
    return {
            'row' : dict_data,
            'email' : email_list
        }
