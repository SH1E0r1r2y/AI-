from flask import Flask, render_template, request
import os
import sys

import requests
import bug1
import re
import constants as constants
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

# Replace this with your OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

app = Flask(__name__)

prompt = """
You are a web security expert tasked with examining a web page to determine if it is a phishing site or a legitimate site:
You are given with an URL.
Fetch the HTML of the given URL and analyze the HTML, URL for any techniques often used in phishing attacks.
Identify the brand name. If the HTML appears to resemble a legitimate web page, verify if the URL matches the legitimate domain name associated with the brand, if known.
Submit your findings as JSON-formatted output with the following keys:
phishing_score: int (indicates phishing risk on a scale of 0 to 10)
brands: str (identified brand name or None if not applicable)
phishing: boolean (whether the site is a phishing site or a legitimate site)
suspicious_domain: boolean (whether the domain name is suspected to be not legitimate)
    """


@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        user_input = request.form["user_input"]
        # 使用正則表達式進行 URL 提取
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, user_input)
        if urls:
            # 得到 url 內的 html 並儲存到 filtered_data.txt
            try:
                for url in urls:
                    html_content = bug1.get_html(url)  # 在 url 的陣列裡面
                    Total_text = bug1.get_text(html_content)
                    output_folder = 'weeeb/data/filtered_data.txt'
                    with open(output_folder, 'w', encoding='utf-8') as text_file:
                        text_file.write(Total_text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                return None

            # 若提取到 URL，將其添加到聊天歷史中，並使用 ConversationalRetrievalChain 進行回答處理
            query = f"{prompt}\nHTML:\n{user_input}\n"
            result = chain({"question": query, "chat_history": chat_history})
            chat_history.append((query, result['answer']))
            return render_template("index.html", response_text=result['answer'], extracted_urls=urls)
        else:
            # 若未提取到 URL，僅顯示回答結果，不添加到聊天歷史中
            query = f"{prompt}\nHTML:\n{user_input}\n"
            result = chain({"question": query, "chat_history": chat_history})
            return render_template("index.html", response_text=result['answer'], extracted_urls=None)

    return render_template("index.html", response_text=None, extracted_urls=None)


def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()


if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist",
                         embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader("weeeb/data/")
    if PERSIST:
        index = VectorstoreIndexCreator(
            vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

if __name__ == "__main__":
    app.run(debug=True)
