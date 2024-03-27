import os
import pyodbc
import time
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from neo4j import GraphDatabase

class Helper_Class:
    def __init__(self):
        # Load environment variables
        load_dotenv(override=True)
        # Azure Db Configuration
        self.server = os.environ["SERVER_URL"]
        self.database = os.environ["DATABASE_NAME"]
        self.username = os.environ["DATABASE_USERNAME"]
        self.password = os.environ["DATABASE_PASSWORD"]
        # Azure Blob Configuration
        self.blob_connection_string = os.environ["BLOB_CONNECTION_STRING"]
        self.blob_container_name = os.environ["BLOB_CONTAINER_NAME"]
        # Azure OpenAI & Search AI Configuration
        self.credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]) if len(os.environ["AZURE_SEARCH_ADMIN_KEY"]) > 0 else DefaultAzureCredential()
        self.api_type = os.environ["API_TYPE"]
        self.api_base = os.environ["AZURE_OPENAI_ENDPOINT"]
        self.api_version = os.environ["AZURE_API_VERSION"]
        self.api_key = os.environ["AZURE_OPENAI_API_KEY"]
        self.deployment_id = os.environ["AZURE_OPENAI_DEPLOYMENT_ID"]
        self.search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
        self.search_key = os.environ["AZURE_SEARCH_ADMIN_KEY"]
        self.search_index_name_sql = os.environ["AZURE_SEARCH_INDEX_SQL"]
        self.search_index_name_blob = os.environ["AZURE_SEARCH_INDEX_BLOB"]
        self.embedding_deployment_id = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID"]
        # Neo4j Configuration
        self.neo4j_url = os.environ["NEO4J_URL"]
        self.neo4j_username = os.environ["NEO4J_USERNAME"]
        self.neo4j_password = os.environ["NEO4J_PASSWORD"]
        self.neo4j_db = os.environ["NEO4J_DATABASE"]
        # Initialize Blob Service Client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.blob_connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.blob_container_name)
        # connect Neo4j DB
        self.driver = GraphDatabase.driver(self.neo4j_url, auth=(self.neo4j_username, self.neo4j_password),database=self.neo4j_db)
        # Azure Api Client
        self.client = AzureOpenAI(
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version = os.getenv("AZURE_API_VERSION"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    
    def connect_to_database(self):
        retry_count = 0
        while True:
            try:
                self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';ENCRYPT=yes;UID='+self.username+';PWD='+self.password)
                print("Database connection established successfully!")
                break
            except pyodbc.OperationalError as e:
                if retry_count >= self.max_retries:
                    print(f"Maximum retries ({self.max_retries}) exceeded. Unable to establish database connection.")
                    raise e
                else:
                    print(f"Database connection attempt {retry_count+1} failed. Retrying in {self.retry_delay} seconds...")
                    retry_count += 1
                    time.sleep(self.retry_delay)