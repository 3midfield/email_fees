# ForUsAll AI Marketing Agent

## Collaborators and Roles:

 - Alexander Adams(alexander-adams1)
    - AWS and Google Search Functionality
 - Kenneth Frisard(3midfield)
    - Pinecone Functionality and Email Cadence Optimization

## Description

 This project creates marketing emails for a csv list of potential customers that have accessed the ForUsAll's website. Taking a contact list from zoominfo in a csv format, we are able to parse through the csv, research the companies, and create a personalized email cadence that sends emails through Hubspot. 

## Documents:

 - serverless.yml
 - testing.py
 - google_search.py
 - post_sqs.py
 - send_approval.py
 - tasktoken.py 
 - hubspot_send.py
 - step_failure.py
 - email_push.py

 ## Resources:

 - Pinecone
 - GPT-4
 - Hubspot
 - AWS

 ## AWS Resources:
 - API Gateway
 - Lambda
 - Step Functions
 - DynamoDB Tables
 - Lambda Layers(For Dependencies)
 - S3 Bucket
 - Amazon EventBridge

## Instructions:

The user drops a json template into the ForUsAll AWS S3 bucket **second-fua-csv-bucket-ai-agent**(or uses an already existing json) containing the necessary email queries. Afterwards, the user will drop a csv file corresponding to the json file. The naming conventions are linked below:

https://docs.google.com/document/d/10lFlZNylnprPLJpM-fj-e4PfcQaPDqniltNakgJQ5Hw/edit?usp=sharing

Afterwards, an email will be sent to the user with the marketing emails which must be approved or rejected. If rejected, the emails are not sent out, and if approved, the emails are sent out through hubspot. 

## Project Code Layout:

The S3 bucket triggers the ***testing.py*** lambda function which checks if both a csv and its corresponding json are present, then proceeds to trigger the step function **FullUnderscoreaiUnderscoreagentStepFunctionsStateMachine-vJkfuNkf7JGX**. The step function takes in the csv file and json, mapping through the csv file. First, it invokes ***google_search.py*** which researches all the companies then parses through the relevant information. The next lambda function ***post_sqs.py*** adds the information to pinecone, and then invokes ***email_push.py***, which creates the email cadence using relevant information. 

After we have parsed the csv file, an email is sent with all the emails to be approved by an individual within the ForUsAll Sales' Team through ***send_approval.py***. The email recipient must click an approve or reject URL to either send out the emails or refrain from sending the emails for a variety of reasons. This action will trigger the lambda function ***tasktoken.py***, which will either continue the step function or terminate depending on the link clicked(accept or reject). If accepted, the email forms will be filled out in order to send the requests to hubspot through the lambda function ***hubspot_send.py***.

Additionally, if at any point the step function fais, the Amazon EventBridge Rule **ai-agent-marketing-dev-StepFunctionFailureRule-1UYA24JCKGGA1** triggers the lambda function ***step_failure.py*** which sends an email to the same individuals who must accept or reject the emails that the step function has failed. This notification is also sent after the user rejects the emails.  


