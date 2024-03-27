from .chat_bot import ChatBotAssistant
import os
import time

class ChatBotHistory(ChatBotAssistant):
    def __init__(self):
        super().__init__()
        # Initialize variables for chat history
        self.name = 'Assistant'
        self.explicit_input = ""
        self.chat_history = ''
        self.chatgpt_output = 'Chat log: /n'
        cwd = os.getcwd()
        i = 1

        # Find an available chat history file
        while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
            i += 1

        self.history_file = os.path.join(cwd, f'chat_history{i}.txt')

        # Create a new chat history file
        with open(self.history_file, 'w') as f:
            f.write('\n')

    # Function to handle user chat input
    def chat(self, user_input):
        current_day = time.strftime("%d/%m", time.localtime())
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.chat_history += f'\nUser: {user_input}\n'
        chatgpt_raw_output = self.create_completion(user_input, self.explicit_input, self.chat_history).replace(f'{self.name}:', '')
        self.chatgpt_output = f'{self.name}: {chatgpt_raw_output}'
        self.chat_history += self.chatgpt_output + '\n'
        with open(self.history_file, 'a') as f:
            f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  self.chatgpt_output + '\n')
            f.close()
        return chatgpt_raw_output

    # Function to get a response from the chatbot
    def get_response(self, userText):
        return self.chat(userText)
