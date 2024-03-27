import time
import logging
from flask import request, redirect, Blueprint, jsonify
from modules.stock_news import StocknewsDataloader

datasource_bp = Blueprint('datasource_bp', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@datasource_bp.route('/data_source', methods=['POST'])
def run_data_loaders():
    max_retries = 3 
    retry_delay = 60 
    
    retries = 0
    while retries < max_retries:
        try:
            Stocknews = StocknewsDataloader()
            Stocknews.fetch_and_save_data()
            # Perform actions with Stocknews object here
            logger.info("Data loaded successfully from Stocknews.")
            return jsonify({"message": "Data loaded successfully"}), 200
        except Exception as e:
            logger.error("Error occurred while loading data from Stocknews: %s", e)
            retries += 1
            if retries < max_retries:
                logger.info("Retrying in %d seconds...", retry_delay)
                time.sleep(retry_delay)
    else:
        logger.error("Maximum retries reached. Unable to load data.")
        return jsonify({"error": "Maximum retries reached. Unable to load data."}), 500
