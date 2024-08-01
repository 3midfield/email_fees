# chain = RetrievalQA.from_chain_type(
#   llm=ChatOpenAI(temperature=0.8, model="gpt-3.5", manx_tokens=512),
#   chain_type="stuff",
#   retriever=index.vectorstore.as_retriever()
# )


# with open('Steam_Logistics.csv') as csv_file:
#     dataframe = pd.read_csv(csv_file)
#     firsti = dataframe['First Name']
#     secondi = dataframe['Last Name']
#     print(len(dataframe))
#     print(len(firsti))
#     for i in range(len(dataframe)):
#         print(firsti[i])
#         query = 'write an email marketing ForUsAll to ' + firsti[i] + ' ' + secondi[i]
#         print(query)
#         print(chain.run(query))
    

# print(chain.run(query))