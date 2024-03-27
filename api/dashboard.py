from flask import request, jsonify, Blueprint
from modules.query_generation import Neo4jGPTQuery
from modules.summary_generation import SummaryGenrationAssistant
from modules.keytake_generation import KeyTakeAwaysGenrationAssistant

knowledge_bp = Blueprint('knowledge_bp', __name__,)
 
gds_db = Neo4jGPTQuery()
gds_db.generate_schema()
summary_generation = SummaryGenrationAssistant()
key_takeaway = KeyTakeAwaysGenrationAssistant()
summary_generation.setup_openai()
key_takeaway.setup_openai()


# Define a route to handle incoming requests
@knowledge_bp.route('/kg/query', methods=['GET'])
def query_handler():

    query = request.args.get('word')

    if query:
        # Process the query using your functions
        neo4j_response = gds_db.run(query)
        summary_response = summary_generation.create_completion(query)
        keytakeaways = key_takeaway.create_completion(query)
        keytakeaways_response = keytakeaways.split('\n')
        
        # Combine both responses
        combined_response = {
            'Kg-Response': neo4j_response,
            'Summary': summary_response,
            'Keytake-Aways': keytakeaways_response
        }
        
        return jsonify(combined_response)
    else:
        # If query word is not provided, return an error message
        return jsonify({'error': 'Query word is missing'}), 400