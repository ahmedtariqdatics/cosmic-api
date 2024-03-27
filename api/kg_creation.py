from flask import request, redirect, Blueprint,jsonify
from modules.kg_index import llama_index

kg_creation_bp = Blueprint('kg_creation_bp', __name__)

@kg_creation_bp.route('/graph', methods=['POST'])
def create_llama_index():
    llama_index.setup_llms()
    documents = llama_index.load_data()
    storage_context = llama_index.create_graph_store()
    index = llama_index.create_index(documents, storage_context)
    return jsonify({"message": f"Llama index created with {len(documents)} documents"}), 200

# Example of handling errors
@kg_creation_bp.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Resource not found"}), 404

