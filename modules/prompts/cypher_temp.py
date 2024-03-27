node_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect(property) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output

"""

rel_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect(property) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
"""

rel_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "node"
RETURN {source: label, relationship: property, target: other} AS output
"""

cypherQueries_example = """
MATCH (n:Entity {id: 'John'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'Google'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'HarryPotter'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'USA'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'TomHanks'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'Elephant'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'StephenKing'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'Flour'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'Messi'})-[r]-(m:Entity) RETURN n, type(r), m
MATCH (n:Entity {id: 'LeonardoDaVinci'})-[r]-(m:Entity) RETURN n, type(r), m
"""

def schema_text(node_props, rel_props, rels):
    return f"""
  This is the schema representation of the Neo4j database.
  Node properties are the following:
  {node_props}
  Relationship properties are the following:
  {rel_props}
  Relationship point from source to target nodes
  {rels}
  Make sure to respect relationship types and directions
  """