import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from openai import OpenAI
from neo4j import GraphDatabase
#from textblob import TextBlob

df_path = "/workspaces/stack-ai-chatbot-error-analysis/data/predicting_students_errors.csv"


loader = DirectoryLoader(COURSES_PATH, glob="**/lesson.adoc", loader_cls=TextLoader)
docs = loader.load()

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1500,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)

# Create a function to get the embedding
def get_embedding(llm, text):
    response = llm.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
    return response.data[0].embedding

# Create a function to get the course data


# Create OpenAI object
llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Connect to Neo4j
driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(
        os.getenv('NEO4J_USERNAME'),
        os.getenv('NEO4J_PASSWORD')
    )
)
driver.verify_connectivity()

# Create a function to run the Cypher query


# Iterate through the chunks and create the graph
for chunk in chunks:
    with driver.session(database="neo4j") as session:
        
        session.execute_write(
            create_chunk,
            get_course_data(llm, chunk)
        )

# Close the neo4j driver
driver.close()