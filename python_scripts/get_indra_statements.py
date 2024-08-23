import json
from indra.sources import reach


def main():
    # All the code that you currently have running at the top level
    results = reach.process_pmc('PMC3898398')
    statements = results.statements
    statements_json = [stmt.to_json() for stmt in statements]
    with open("results/pmc3898398/indra_results.json", "w") as file:
        json.dump(statements_json, file, indent=4)

    return statements_json


if __name__ == "__main__":
    statements_json = main()
    print(statements_json)
