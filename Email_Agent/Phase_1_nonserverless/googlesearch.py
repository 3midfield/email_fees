from googleapiclient.discovery import build
import json
import pandas as pd
from langchain.document_loaders import WebBaseLoader


# Google Search API Key: AIzaSyC7Pzfb-S3Z6YIjtXC2CZYAAvUxR-_3Hgs
# Google Search Engine ID: 6064656ace39e41fc

# Could even add the WebBaseLoader if more information is needed after our

list = []
service = build('customsearch', 'v1', developerKey='AIzaSyCjvYaLI190wdKwqlq8vgXBqdMFKhEl_iU')
with open('/Users/alexanderadams/ForUsAll-1/first_5.csv') as csv_file:
    # should be organized.csv when actually running(this is just for training)
    dataframe = pd.read_csv(csv_file)
    name = dataframe['Company Name']
    website = dataframe['Website']
    for i in range(len(dataframe)):
        if name[i] in list:
            print('found in list')
        else:
            list.append(name[i])
            res=(service.cse().list(q='summary of ' + name[i] , cx="6064656ace39e41fc").execute())
            string = '/Users/alexanderadams/ForUsAll-1/files/' + name[i] + '.txt'
            mission = (service.cse().list(q= name[i] + ' mission' , cx="6064656ace39e41fc").execute())
            content = json.dumps(res) 
            data1 = json.loads(content)
            
            content2 = json.dumps(mission)
            data2=json.loads(content2)
            relevant_texts = ''
# Save the results to a file
            with open(string, 'w') as f:
                f.write(content + content2) 

