# if PERSIST and os.path.exists("persist"):
#   print("Reusing index...\n")
#   vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
#   from langchain.indexes.vectorstore import VectorStoreIndexWrapper
#   index = VectorStoreIndexWrapper(vectorstore=vectorstore)
# else:
#   loader = CSVLoader('Steam_Logistics.csv')
#   # This code can also import folders, including various filetypes like PDFs using the DirectoryLoader.
#   # loader = DirectoryLoader(".", glob="*.txt")
#   if PERSIST:
#     index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader, apify_loader])
#   else:
# index = VectorstoreIndexCreator().from_loaders([loader, apify_loader])
