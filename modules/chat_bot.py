import os
from modules.helper_module import Helper_Class
import openai

class ChatBotAssistant(Helper_Class):

    def setup_openai(self):
        self.client = openai.AzureOpenAI(
                base_url=f"{self.api_base}/openai/deployments/{self.deployment_id}/extensions",
                api_key=self.api_key,
                api_version=self.api_version,
            )
        
    def create_completion(self, user_input, explicit_input, chat_history):

        user_message = f"Question:{user_input}"
        
        system_message = f"""
        You are an AI Chat Assistant for Market Pulse. To give assistance for Customer Services.
            Instructions:
            1. Maintain a persuasive and professional tone in all interactions.
            2. Refrain from initiating responses with phrases like 'In the given text' or 'Provided input text.'
            3. Adhere to these guidelines for effective communication as a Customer Services chatbot.
        """
        completion = self.client.chat.completions.create(
            model=self.deployment_id,
            messages=[
                {"role": "system", "content": f"{system_message}. Conversation history: {chat_history}"},
                {"role": "user", "content": f"{user_message}.{explicit_input}"}
                ],
            extra_body={
                "dataSources": [
                    {
                        "type": "AzureCognitiveSearch",
                        "parameters": {
                            "endpoint": os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"],
                            "key": os.environ["AZURE_SEARCH_ADMIN_KEY"],
                            "indexName": os.environ["AZURE_SEARCH_INDEX_SQL"],
                            "queryType": "vectorSimpleHybrid",
                            #"fieldsMapping": {
                            #        "contentFieldsSeparator": "\n",
                            #        "contentFields": ["parent_sentiment"],
                            #        "filepathField": "Id",
                            #        "titleField": "parent_title",
                            #        "urlField": "parent_Url",
                            #        "vectorFields": ["vector"]
                            #},
                            "inScope": True,
                            "filter": None,
                            "roleInformation": system_message,
                            "strictness": 3,
                            "topNDocuments": 10,
                            "embeddingDeploymentName": "text-embedding-ada-002"
                        }
                    }
                ]
            }
        )
        context = completion.choices[0].message.content
        return context