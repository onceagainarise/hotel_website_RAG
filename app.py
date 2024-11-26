#this code retrieve the data from the database

import os  
from flask import Flask, render_template, redirect, url_for, request
from langchain_pinecone import PineconeEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Pinecone and Groq API
pinecone_api_key = os.getenv("PINECONE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")  # Replace with your actual key

pc = Pinecone(api_key=pinecone_api_key)
llm_groq = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.2-3b-preview")

# Pinecone index name
PINECONE_INDEX_NAME = "car-data-index"


# Ensure Pinecone index exists
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    print(f"Index '{PINECONE_INDEX_NAME}' does not exist. Create the index first.")
    exit(1)

# Initialize PineconeEmbeddings for retrieval
embeddings = PineconeEmbeddings(model="multilingual-e5-large")

# Initialize Pinecone vector store with embedding function
vector_store = PineconeVectorStore(
    index=pc.Index(PINECONE_INDEX_NAME),
    embedding=embeddings  # Provide the embedding function for retrieval
)

# Configure LangChain with Groq and Pinecone
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = ConversationalRetrievalChain.from_llm(
    llm=llm_groq, retriever=vector_store.as_retriever(), memory=memory
)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    answer = ""
    source_documents = []

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            response = chain.invoke({"question": user_input})
            answer = response.get("answer", "No answer available.")
            source_documents = response.get("source_documents", [])

    return render_template("chat.html", answer=answer, source_documents=source_documents)

if __name__ == "__main__":
    app.run(debug=True)
