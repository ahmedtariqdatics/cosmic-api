from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserCred(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

class UserProfile(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user_cred.id'), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_no = db.Column(db.String(50))
    region = db.Column(db.String(50))
    language = db.Column(db.String(50))
    image_id = db.Column(db.Integer, db.ForeignKey('user_images.image_id'))

class UserImages(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_blob_url = db.Column(db.String(500))

class ChatHistory(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user_cred.id'))
    chat_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)

class ChatMessages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat_history.chat_id'))
    message_content = db.Column(db.Text)
    message_timestamp = db.Column(db.DateTime)

class NewsMetaData(db.Model):
    news_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    ticker = db.Column(db.String(20), db.ForeignKey('stock_market.ticker'))
    published_on = db.Column(db.DateTime)
    url = db.Column(db.String(500))
    summary = db.Column(db.Text)
    sentiment = db.Column(db.String(10))
    source = db.Column(db.String(50))
    image_url = db.Column(db.String(500))

class StockStats(db.Model):
    stock_id = db.Column(db.String(50), primary_key=True)
    ticker = db.Column(db.String(20), db.ForeignKey('stock_market.ticker'))
    previous_close = db.Column(db.String(50))
    day_range = db.Column(db.String(50))
    year_range = db.Column(db.String(50))
    market_cap = db.Column(db.String(50))
    avg_volume = db.Column(db.String(50))
    p_e_ratio = db.Column(db.String(50))
    primary_exchange = db.Column(db.String(50))
    company_category = db.Column(db.String(50))
    trends_category = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime)

class StockMarket(db.Model):
    companytitle = db.Column(db.String(50))
    ticker = db.Column(db.String(20), primary_key=True)
    trading = db.Column(db.String(50))
    extracted_price = db.Column(db.Float)
    currency = db.Column(db.String(10))
    price = db.Column(db.String(50))
    percentage = db.Column(db.Float)
    value = db.Column(db.Float)
    movement = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime)

class Watchlist(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user_cred.id'), primary_key=True)
    ticker = db.Column(db.String(20), db.ForeignKey('stock_market.ticker'), primary_key=True)
    category = db.Column(db.String(50))
