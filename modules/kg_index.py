import os
from llama_index.core import StorageContext, KnowledgeGraphIndex, Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.readers.azstorage_blob import AzStorageBlobReader
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from modules.helper_module import Helper_Class

class LlamaIndex(Helper_Class):

    def setup_llms(self):
        llm = AzureOpenAI(
            model="gpt-35-turbo-16k",
            deployment_name=self.deployment_id,
            api_key=self.api_key,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_API_VERSION"),
        )
        embedding_llm = AzureOpenAIEmbedding(
            model="text-embedding-ada-002",
            deployment_name=self.embedding_deployment_id,
            api_key=self.azure_openai_key,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_API_VERSION"),
        )
        Settings.llm = llm
        Settings.embed_model = embedding_llm
        Settings.chunk_size = 512

    def load_data(self):
        loader = AzStorageBlobReader(
            container_name=self.blob_container_name,
            connection_string=self.blob_connection_string,
        )
        return loader.load_data()

    def create_graph_store(self):
        graph_store = Neo4jGraphStore(
            username=self.neo4j_username,
            password=self.neo4j_password,
            url=self.neo4j_url,
            database=self.neo4j_db,
        )
        return StorageContext.from_defaults(graph_store=graph_store)

    def create_index(self, documents, storage_context):
        return KnowledgeGraphIndex.from_documents(
            documents,
            storage_context=storage_context,
            max_triplets_per_chunk=3,
            include_embeddings=True,
            show_progress = True,
            refresh_ref_docs = True

        )

