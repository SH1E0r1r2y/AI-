import sys
from flask import Flask, render_template, request
import os
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import constants

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = constants.APIKEY

PERSIST = True
query = None
if len(sys.argv) > 1:
    query = sys.argv[1]
prompt = """
You are a web security expert tasked with examining a web page to determine if it is a phishing site or a legitimate site:
You are given with an URL.
Fetch the HTML of the given URL and analyze the HTML, URL for any techniques often used in phishing attacks.
Identify the brand name. If the HTML appears to resemble a legitimate web page, verify if the URL matches the legitimate domain name associated with the brand, if known.
Submit your findings as JSON-formatted output with the following keys:
Url:str (the url be analysised)
phishing_score: int (indicates phishing risk on a scale of 0 to 10)
brands: str (identified brand name or None if not applicable)
phishing: boolean (whether the site is a phishing site or a legitimate site)
suspicious_domain: boolean (whether the domain name is suspected to be not legitimate)
"""

chat_history = []  # 須為全域變數


# 要放在 chatbot 裡面
if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist",
                         embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    # loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
    loader = DirectoryLoader("data/")
    if PERSIST:
        index = VectorstoreIndexCreator(
            vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),  # 選擇一個合適的 GPT-3.5 引擎
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)


@app.route("/", methods=["GET", "POST"])
def chatbot():
    global query  # 添加到全域變數
    global chat_history

    if request.method == "POST":
        user_input = request.form.get("user_input")
        query = f"{prompt}URL:\n{user_input}\n"

        result = chain({"question": query, "chat_history": chat_history})
        response_text = result["answer"]

        chat_history.append((query, response_text))
        query = None
        # import JSON 檔案並增加safe/warning 分類
        return render_template("index.html", response_text=response_text)

    return render_template("index.html", response_text=None)


if __name__ == "__main__":
    chat_history = []
    # 增加 user_input
    app.run(debug=True, port=500)
