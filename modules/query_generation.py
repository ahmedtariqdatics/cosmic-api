import json
from neo4j.exceptions import CypherSyntaxError
from .prompts.cypher_temp import node_properties_query,rel_properties_query,rel_query,schema_text,cypherQueries_example
from modules.helper_module import Helper_Class

class Neo4jGPTQuery(Helper_Class):
    
    def generate_schema(self):
        node_props = self.query_database(node_properties_query)
        rel_props = self.query_database(rel_properties_query)
        rels = self.query_database(rel_query)
        return schema_text(node_props, rel_props, rels)

    def refresh_schema(self):
        self.schema = self.generate_schema()

    def get_system_message(self):
        return f"""
        Task: 
        Generate Cypher queries to query a Neo4j graph database based on the provided schema definition.
        Instructions:
        Use only the provided relationship types and properties.
        Do not use any other relationship types or properties that are not provided.
        Do not change the user query search as it is.
        If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
        Schema:
        {self.schema}
        Cypher queries Example:
        {cypherQueries_example}
        Follow the Cypher Queries Example to make more accurate cypher Queries.
        Note: Do not include any explanations or apologies in your responses.
        """

    def query_database(self, neo4j_query, params={}):
        with self.driver.session() as session:
            result = session.run(neo4j_query, params)
            #output = [r.values() for r in result]
            #output.insert(0, result.keys())
            output = []
            for record in result:
                output.append(record.data())
            return json.dumps(output)
            
    def construct_cypher(self, question, history=None):
        messages = [
            {"role": "system", "content": self.get_system_message()},
            {"role": "user", "content": question},
        ]
        # Used for Cypher healing flows
        if history:
            messages.extend(history)

        completions = self.client.chat.completions.create(
            model=self.azure_openai_deployment_id,
            temperature=0.0,
            messages=messages
        )
        return completions.choices[0].message.content

    def run(self, question, history=None, retry=True):
        # Construct Cypher statement
        cypher = self.construct_cypher(question, history)
        #print(cypher)
        try:

            return self.query_database(cypher)
        # Self-healing flow
        except CypherSyntaxError as e:
            # If out of retries
            if not retry:
              return "Invalid Cypher syntax"
            print("Retrying")
            return self.run(
                question,
                [
                    {"role": "assistant", "content": cypher},
                    {
                        "role": "user",
                        "content": f"""This query returns an error: {str(e)} 
                        Give me a improved query that works without any explanations or apologies""",
                    },
                ],
                retry=False
            )
        
# Example usage:
#if __name__ == "__main__":
#    gds_db = Neo4jGPTQuery()
#    results = gds_db.run("apple")
#    print(results)