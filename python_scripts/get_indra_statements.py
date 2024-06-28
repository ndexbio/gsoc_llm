import json
from indra.sources import indra_db_rest

results = indra_db_rest.get_statements_for_papers([('pmcid', 'PMC333362')])
# Access the statements
statements = results.statements

# Convert statements to a JSON serializable format
statements_json = [stmt.to_json() for stmt in statements]

# Write the statements to a JSON file
with open("results.json", "w") as file:
    json.dump(statements_json, file, indent=4)
