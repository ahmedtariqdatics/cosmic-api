import logging
from flask import Flask, Blueprint, jsonify
from config import ProductionConfig
from model import db
from modules.financial_matrix import StockDataFetcher

financial_data_bp = Blueprint('financial_data_bp', __name__)

app = Flask(__name__)
app.config.from_object(ProductionConfig)
db.init_app(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@financial_data_bp.route('/stock_data', methods=['GET'])
def run_data_loaders():
    try:
        # Pass the Flask app and SQLAlchemy instance to StockDataFetcher
        stock_data_fetcher = StockDataFetcher(app, db)
        stock_data_fetcher.fetch_and_save_data()
        logger.info("Data loaded successfully from Stocknews")
        return jsonify({"message": "Data loaded successfully"}), 200
    except Exception as e:
        logger.error("Error occurred while loading data from Stocknews: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500
