from flask import Flask, render_template, request
import os
import sys
import constants
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True
query = None
if len(sys.argv) > 1:
    query = sys.argv[1]

# Modify the prompt to include the new instructions and input fields
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
example if I input http://execrealtitle.repairtheac.com/execrealtitle,You give me：
{
  "url": "http://execrealtitle.repairtheac.com/execrealtitle",
  "phishing_score": 8,
  "brands": "None",
  "phishing": true,
  "suspicious_domain": true
}
"""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chatbot():
    global chat_history

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist",
                             embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = DirectoryLoader("gpt-master/data/")
        if PERSIST:
            index = VectorstoreIndexCreator(
                vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )


    if request.method == "POST":
        user_input = request.form.get('user_input')
        chat_history = []
        # Pass the user's URL input to the ConversationalRetrievalChain
        query = f"{prompt}URL:\n{user_input}\n"
        
        print("query=",query)

        # Get the response from the chatbot
        result = chain({"question": query, "chat_history": chat_history})
        response_text = result["answer"]

        # Append the query and response to the chat history
        chat_history.append((query, response_text))
        query = None

        # Parse the JSON response from the chatbot
        import json
        response_json = json.loads(response_text)

        # Check if "phishing" is true and display warning text accordingly
        if "phishing" in response_json and response_json["phishing"]:
            warning_text = '<p class="red-text"><i class="fas fa-exclamation-triangle"></i> Warning!!!</p>'
        else:
            warning_text = '<p class="green-text"><i class="fas fa-check-circle"></i> Safe</p>'

        # Render the template with the response JSON and warning_text
        return render_template("index.html", response_text=json.dumps(response_json, indent=2), warning_text=warning_text)


    return render_template("index.html", response_text=None)


if __name__ == "__main__":
    chat_history = []
    user_input=""
    query = None
    app.run(debug=True,port = 500)
