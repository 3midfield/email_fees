import json
import requests

def push_to_hubspot(email_list, dataframe):
    company = dataframe['Company Name']
    website = dataframe['Website']
    first_name = dataframe['First Name']
    last_name = dataframe['Last Name']
    email = dataframe['Email Address']

    
    address = dataframe['Full Address']
    job_title = dataframe["Job Title"]
    phone_number = dataframe["Direct Phone Number"]
    mobile_number = dataframe["Mobile phone"]
    zoom_info_contact = dataframe["ZoomInfo Contact Profile URL"]
    linkedin_contact = dataframe["LinkedIn Contact Profile URL"]
    revenue = dataframe["Revenue (in 000s USD)"]
    employees = dataframe["Employees"]
    zoom_info_company = dataframe["ZoomInfo Company Profile URL"]
    linkedin_company = dataframe["LinkedIn Company Profile URL"]
    department = dataframe["Department"]
    access_token = 'pat-na1-d0ccbb98-5138-481c-802f-5883dd9e5a2b'
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    data = {
        "fields": [
        {
        "objectTypeId": "0-1",
        "name": "lastname",
        "value": str(last_name)
        },
        {
        "objectTypeId": "0-1",
        "name": "firstname",
        "value": str(first_name)
        },
        {
        "objectTypeId": "0-1",
        "name": "jobtitle",
        "value": str(job_title)
        },
        {
        "objectTypeId": "0-1",
        "name": "direct_phone",
        "value": str(phone_number)
        },
        {
        "objectTypeId": "0-1",
        "name": "email",
        "value": str(email)
        },
        {
        "objectTypeId": "0-1",
        "name": "department",
        "value": str(department)
        },
        {
        "objectTypeId": "0-1",
        "name": "mobilephone",
        "value": str(mobile_number)
        },
        {
        "objectTypeId": "0-1",
        "name": "zoominfo_contact_profile_url",
        "value": str(zoom_info_contact)
        },
        {
        "objectTypeId": "0-1",
        "name": "person_linkedin_url__c",
        "value": str(linkedin_contact)
        },
        {
        "objectTypeId": "0-1",
        "name": "company",
        "value": str(company)
        },
        {
        "objectTypeId": "0-1",
        "name": "website",
        "value": str(website)
        },
        {
        "objectTypeId": "0-2",
        "name": "company_revenues",
        "value": str(revenue)
        },
        {
        "objectTypeId": "0-1",
        "name": "company_size",
        "value": str(employees)
        },
        {
        "objectTypeId": "0-2",
        "name": "zoominfo_company_profile_url",
        "value": str(zoom_info_company)
        },
        {
        "objectTypeId": "0-2",
        "name": "company_linkedin_url__c",
        "value": str(linkedin_company)
        },
        {
        "objectTypeId": "0-1",
        "name": "address",
        "value": str(address)
        },
        {
        "objectTypeId": "0-1",
        "name": "subject_1",
        "value": str(email_list[0])
        },
        {
        "objectTypeId": "0-1",
        "name": "email_body_1",
        "value": email_list[1]
        },
        {
        "objectTypeId": "0-1",
        "name": "subject_2",
        "value": str(email_list[2])
        },
        {
        "objectTypeId": "0-1",
        "name": "email_body_2",
        "value": email_list[3]
        },
        {
        "objectTypeId": "0-1",
        "name": "subject_3",
        "value": str(email_list[4])
        },
        {
        "objectTypeId": "0-1",
        "name": "email_body_3",
        "value": email_list[5]
        },
        {
        "objectTypeId": "0-1",
        "name": "subject_4",
        "value": str(email_list[6])
        },
        {
        "objectTypeId": "0-1",
        "name": "email_body_4",
        "value": email_list[7]
        }]
    }
    return data
    # submission = requests.post('https://api.hsforms.com/submissions/v3/integration/submit/5352904/24ed8f28-e0e0-4160-b599-cae31e8880b4', headers=headers, data = json.dumps(data))
    # print(submission)

def send(event, context):
    # TODO implement
    
    emails = event['email']
    row = event['row']
    
    data = push_to_hubspot(emails, row)
    print(data)
    access_token = 'pat-na1-d0ccbb98-5138-481c-802f-5883dd9e5a2b'
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    submission = requests.post('https://api.hsforms.com/submissions/v3/integration/submit/5352904/24ed8f28-e0e0-4160-b599-cae31e8880b4', headers=headers, data = json.dumps(data))
    print(submission)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }