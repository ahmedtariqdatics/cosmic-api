import os
import requests
import uuid
from datetime import datetime
import time
from bs4 import BeautifulSoup
from modules.helper_module import Helper_Class


class StocknewsDataloader(Helper_Class):

    def fetch_data(self,ticker):
        
        url = "https://stocknewsapi.com/api/v1"
        params = {
            "tickers": ticker,
            "items": 40,
            "page": 1,
            "type":"article",
            "token": "hq52fhmxjpuw2qpgfwa0krw4067af4vjcrocwmpb"
        }
        # Send request to get the data
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []
    
    def save_data(self, news_items,ticker):
        cursor = self.conn.cursor()

        # Check if table exists, if not create it
        cursor.execute("SELECT OBJECT_ID('NewsMetaData') AS TableExists")
        table_exists = cursor.fetchone()
        if not table_exists[0]:
            create_table_query = '''
            CREATE TABLE NewsMetaData (
                Id VARCHAR(255) PRIMARY KEY,
                Title NVARCHAR(MAX),
                Ticker NVARCHAR(MAX),
                PublishedOn DATE,
                Sentiment NVARCHAR(MAX),
                Source NVARCHAR(MAX),
                Summary NVARCHAR(MAX),
                Url NVARCHAR(MAX)
            )
            '''
            cursor.execute(create_table_query)
            self.conn.commit()
            print("NewsMetaData table created")

        for news_item in news_items['data']:
            Id = str(uuid.uuid4())
            Title = news_item['title']
            Ticker = ticker
            PublishedOn = news_item['date']
            Sentiment = news_item['sentiment']
            Source = news_item['source_name']
            Summary = news_item['text']
            Url = news_item['news_url']
            if 'news_url' in news_item:
                Url = news_item['news_url']
            else:
                print("Skipping news item as URL is missing.")
                continue

            final_url = self.fetch_content(Url)
            if final_url:
                soup = BeautifulSoup(final_url, 'html.parser')
                paragraphs = soup.find_all(['p'])
                content = '\n'.join([tag.get_text() for tag in paragraphs])

                formatted_date = datetime.strptime(PublishedOn, "%a, %d %b %Y %H:%M:%S %z").date()

                insert_query = '''
                INSERT INTO NewsMetaData (Id, Title, Ticker, PublishedOn, Sentiment, Source, Summary, Url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(insert_query, (Id, Title,Ticker, formatted_date, Sentiment, Source, Summary, Url))
                self.conn.commit()

                file_name = f"{Source}_{formatted_date}_{Id}.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(content)

                time.sleep(1)

                with open(file_name, "rb") as data:
                    blob_client = self.container_client.get_blob_client(file_name)
                    blob_client.upload_blob(data.read())

                os.remove(file_name)

                print(f"Data for {file_name} inserted into the database and content uploaded to Azure Blob Storage")
        else:
            print("Failed to fetch data for URL:", Url)
            
    def fetch_content(self,url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to fetch data for URL:", url)
                return None
        except Exception as e:
            print("An error occurred while fetching data for URL:", url)
            print(e)
            return None
        
    def fetch_and_save_data(self):
        #tickers = ['META', 'GOOGL', 'AAPL', 'GOOG', 'NVDA', 'TSLA', 'AMZN']
        tickers = ['AMZN']
        for ticker in tickers:
            news_items = self.fetch_data(ticker)
            print(f"Fetching data for ticker: {ticker}")
            if news_items:
                self.save_data(news_items,ticker)
            else:
                print(f"No data found for ticker: {ticker}")
