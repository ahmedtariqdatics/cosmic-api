import os
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery
from .prompts.prompt_temp import instructions_summaries
from modules.helper_module import Helper_Class

class SummaryGenrationAssistant(Helper_Class):

    def setup_openai(self):
        self.client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = os.getenv("AZURE_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
    
    def create_completion(self, message_text):
        results = self.Search_AI(message_text)
        input_text = " "
        for result in results:  
            input_text = input_text + result['chunk'] + " " 
        
        system_message = f"Please answer the question using the provided input text '{input_text}'. Follow the instructions provided: {instructions_summaries}."

        user_message = f"Question:{message_text}"
        completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                model=self.deployment_id,
                temperature = 0
            )
        context = completion.choices[0].message.content
        return context
    
    def Search_AI(self,message_text):
        search_client = SearchClient(self.search_endpoint , self.search_index_name, credential=self.credential)
        vector_query = VectorizableTextQuery(text=message_text, k_nearest_neighbors=1, fields="vector", exhaustive=True)
  
        results = search_client.search(  
            search_text=message_text,  
            vector_queries= [vector_query],
            select=["chunk"],
            top=10
        ) 
        return results 

