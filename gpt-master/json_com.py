import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

# Modify the prompt to include the new instructions and input fields
prompt = """
You are a web security expert tasked with a non-phishing web page 
The given URL is a company often being mimic by phishing sites.
Fetch the HTML of the given URL and analyze the HTML, URL for any techniques often used in phishing attacks.
Identify the brand name. If the HTML appears to resemble a legitimate web page, verify if the URL matches the legitimate domain name associated with the brand, if known.
Submit your findings as JSON-formatted output with the following keys:
url: str (the url be analysised)
phishing_score: int (indicates phishing risk on a scale of 0 to 10)
brands: str (identified brand name or None if not applicable)
phishing: boolean (whether the site is a phishing site or a legitimate site)
suspicious_domain: boolean (whether the domain name is suspected to be not legitimate)
"""

def read_txt_files_in_directory(directory_path):
    file_paths = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory_path, filename)
            file_paths.append(filepath)
    return file_paths

def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == ':wq':
            break
        lines.append(line)
    return '\n'.join(lines)

def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()

def process_url(url):
    chat_history = []
    query = f"{prompt}URL:\n{url}\n"
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])
    chat_history.append((query, result['answer']))
    with open("./report_json./nor02_jsrepo.json", 'a', encoding='utf-8') as out_file:
        out_file.write(f"{result['answer']}\n")

if __name__ == "__main__":
    file_path = "./data/edu_book/normal.txt"
    
    urls = []
    with open(file_path, "r") as file:
        urls = file.readlines()

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        # loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
        loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    for url in urls:
        url = url.strip()
        process_url(url)