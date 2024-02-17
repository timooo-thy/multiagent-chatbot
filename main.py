from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
import json

load_dotenv()
client = OpenAI()


class Enquiry(BaseModel):
    content: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome": "This is the main endpoint for the Cleaner.io chatbot."}

@app.post("/enquire/")
def user_proxy_agent(enquiry: Enquiry) -> dict:
    """Function for the User Proxy Agent of the cleaning company. This function will return and call either the Scheduler or Guardrail agent."""
    input = enquiry.content
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        temperature=0.5,
        max_tokens=150,
        messages=[
            {"role": "system",
                "content": '''You are the User Proxy Agent of a Cleaning Company. 
                Return in json of the following format: {"agent": agent, "service": service}
                You will return either Guardrail or Scheduler in json.
                For agent:
                Return Scheduler if the user wants to schedule a general cleaning appointment.
                For Scheduler:
                Return general_cleaning for service.
                Return Guardrail otherwise.
                For Guardrail:
                Return post_renovation_cleaning if the user message is similar to post renovation cleaning for service.
                Return unknown otherwise.'''},
            {"role": "user", "content": input}
        ]
    )

    response = json.loads(response.choices[0].message.content)

    if response['agent'] == 'Guardrail':
        return guardrail_agent(response['service'])
    else:

        return scheduler_agent(response['service'])
    

def guardrail_agent(service: str) -> dict:
    """Function for the Guardrail Agent of the cleaning company. This function will return a response based on the service indicated."""
    if service == "post_renovation_cleaning":
        return {"response": "We're connecting you with a human agent."}
    else:
        return {"response": "Sorry, we don't offer that service. We only offer post renovation cleaning."}


def scheduler_agent(service: str) -> dict:
    """Function for the Scheduler Agent of the cleaning company. This function will perform similarity search with RAG and simulate an API call for the next availability slot."""
    db = load_faiss_index()
    context = retrieve_context(db, service)
    next_available_slot = available_slots()

    input = [{
    "role": "system",
    "content": f'''You are the Scheduler Agent of a Cleaning Company.
        Use the following knowledge base only when answering-> Price: {context}, Next available slot: {next_available_slot}.
        Return in json of the following format: {{ "response": "Next available slot on ___, and price is ___." }}'''
    }]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        temperature=0.5,
        max_tokens=150,
        messages=input
    )
    return json.loads(response.choices[0].message.content)

    
def generate_embeddings() -> object:
    """Function for generating embeddings from the knowledge base"""
    # Load training data from CSV file
    loader = CSVLoader(
        "data/training_data.csv")
    documents = loader.load()

    # Create a FAISS vector store from the documents
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)

    # Save the vector store to the local directory
    db.save_local("faiss_index")
    return db

def load_faiss_index():
    """Function for loading the FAISS index"""
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("faiss_index", embeddings)
    return db

def retrieve_context(db: object, prompt_input: str) -> list:
    """Function for retrieving context from the knowledge base"""
    similar_response = db.similarity_search(prompt_input, k=1)
    content_arr = [doc.page_content for doc in similar_response]
    return content_arr

def available_slots() -> str:
    """Function for retrieving the next available slot for the user"""
    return "2025-01-01 00:00"