import json
from indra.sources import reach


def convert_indra_to_langchain_format(data):
    transformed_data = []
    for interaction in data['statements']:
        if 'subj' in interaction and 'obj' in interaction and 'evidence' in interaction:
            subj_name = interaction['subj']['name']
            obj_name = interaction['obj']['name']
            interaction_type = interaction['type']
            text = interaction['evidence'][0]['text']  

            transformed_item = {
                'subj': subj_name,
                'obj': obj_name,
                'interaction_type': interaction_type,
                'text': text
            }
            transformed_data.append(transformed_item)

    return transformed_data


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
