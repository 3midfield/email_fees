import json
from bs4 import BeautifulSoup
import pandas as pd

def extract_text_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

     # Replace the following code with your logic to extract the relevant text
    data = json.loads(content)
    relevant_texts = []
    for item in data['items']:
        snippet = item['snippet']
        metatags = item.get('pagemap', {}).get('metatags', [])
        og_description = ''
        for metatag in metatags:
            og_description = metatag.get('og:description', '')
        soup = BeautifulSoup(snippet + ' ' + og_description, 'html.parser')
        text = soup.get_text()
        relevant_texts.append(text)
    print(relevant_texts)
    return relevant_texts

list = []
with open('first_5.csv') as csv_file:
    # should be organized.csv when running (this is just for training)
    dataframe = pd.read_csv(csv_file)
    name = dataframe['Company Name']
    for i in range(len(dataframe)):
        if name[i] in list:
            print('found in list')
        else:
            list.append(name[i])
            string = 'files/' + name[i] + '.txt'
            text = extract_text_from_file(string)
    # Perform any additional text preprocessing if needed
            string = 'restructured/' + name[i] + '.txt'
    # Add the text into restructured folder
            with open(string, 'w') as f:
                f.write(json.dumps(text))