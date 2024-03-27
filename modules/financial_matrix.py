import requests
import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from model import StockMarket, StockStats

class StockDataFetcher:
    def __init__(self,app,db):
        self.app = app
        self.db = db

    def generate_uuid(self):
        return str(uuid.uuid4())

    def fetch_data(self, ticker):
        url = "https://serpapi.com/search.json"
        params = {
            "api_key": "63e0e326cef43639565614207417a8f141cfd388d7397a9d54a418926a80a268",
            "engine": "google_finance",
            "q": ticker + ":NASDAQ",
            "hl": "en",
            "no_cache": "true",
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []

    def save_stock_stats(self, news_items, ticker):
        try:

            knowledge_graph = news_items.get('knowledge_graph', {})
            key_stats = knowledge_graph.get('key_stats', {}) 
            stats = key_stats.get('stats', [])
            stats_dict = {stat['label']: stat['value'] for stat in stats}  

            new_uuid = self.generate_uuid()
            previous_close = stats_dict.get("Previous close")
            day_range = stats_dict.get("Day range")
            year_range = stats_dict.get("Year range")
            market_cap = stats_dict.get("Market cap")
            avg_volume = stats_dict.get("Avg Volume")
            p_e_ratio = stats_dict.get("P/E ratio")
            primary_exchange = stats_dict.get("Primary exchange")
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            # Creating a StockStats object with the extracted values
            stock_stats = StockStats(
                stock_id=new_uuid,
                ticker=ticker,
                previous_close=previous_close,
                day_range=day_range,
                year_range=year_range,
                market_cap=market_cap,
                avg_volume=avg_volume,
                p_e_ratio=p_e_ratio,
                primary_exchange=primary_exchange,
                company_category=None,
                trends_category=None,
                last_updated=last_updated
            )

            self.db.session.add(stock_stats)
            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            print("Database error occurred:", str(e))
        except Exception as e:
            print("An error occurred:", str(e))

    def save_stock_market(self, news_items, ticker):
        try:
            news_item = news_items['summary']  # Access the summary directly since it's a single item
            title = news_item.get('title')
            ticker_symbol = news_item.get('stock')  # Use the 'stock' attribute for ticker symbol
            trading = news_item.get('market', {}).get('trading')
            extracted_price = news_item.get('market', {}).get('extracted_price')
            currency = news_item.get('market', {}).get('currency')
            price = news_item.get('market', {}).get('price')
            percentage = news_item.get('market', {}).get('price_movement', {}).get('percentage')
            value = news_item.get('market', {}).get('price_movement', {}).get('value')
            movement = news_item.get('market', {}).get('price_movement', {}).get('movement')
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            existing_stock_market = StockMarket.query.filter_by(ticker=ticker).first()

            if existing_stock_market:
                # Update existing entry
                existing_stock_market.companytitle = title
                existing_stock_market.trading = trading
                existing_stock_market.extracted_price = extracted_price
                existing_stock_market.currency = currency
                existing_stock_market.price = price
                existing_stock_market.percentage = percentage
                existing_stock_market.value = value
                existing_stock_market.movement = movement
                existing_stock_market.last_updated = last_updated
            else:
                # Create new entry
                stock_market = StockMarket(
                    companytitle=title,
                    ticker=ticker,
                    trading=trading,
                    extracted_price=extracted_price,
                    currency=currency,
                    price=price,
                    percentage=percentage,
                    value=value,
                    movement=movement,
                    last_updated=last_updated
                )
                self.db.session.add(stock_market)

            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            print(f"Ticker '{ticker}' already exists. Updating existing entry instead.")
        except SQLAlchemyError as e:
            self.db.session.rollback()  # Rollback changes if any other DB error occurs
            print("Database error occurred:", str(e))
        except KeyError as e:
            print("KeyError:", str(e))
            print("Check if the structure of 'news_items' matches the expected format.")
        except Exception as e:
            print("An error occurred:", str(e))

    def fetch_and_save_data(self):
        tickers = ['META', 'GOOGL', 'AAPL', 'GOOG', 'NVDA', 'TSLA', 'AMZN']
        #tickers = ['AMZN']
        for ticker in tickers:
            news_items = self.fetch_data(ticker)
            if news_items:
                self.save_stock_market(news_items, ticker)
                self.save_stock_stats(news_items, ticker)
            else:
                print(f"No data found for ticker: {ticker}")

