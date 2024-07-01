import json
from indra.sources import indra_db_rest


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
    results = indra_db_rest.get_statements_for_papers([('pmcid', 'PMC333362')])
    statements = results.statements
    statements_json = [stmt.to_json() for stmt in statements]
    with open("results/pmc333362/indra_results.json", "w") as file:
        json.dump(statements_json, file, indent=4)

    transformed_data = convert_indra_to_langchain_format(statements_json)
    with open("results/pmc333362/conv_indra_results.json", "w") as file:
        json.dump(transformed_data, file, indent=4)

    return statements_json, transformed_data


if __name__ == "__main__":
    statements_json, transformed_data = main()
