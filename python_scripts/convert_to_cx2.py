import pandas as pd
import json
from ndex2.cx2 import PandasDataFrameToCX2NetworkFactory
from ndex2.client import Ndex2


def convert_to_cx2(extracted_results):
    # Initialize lists to store extracted data
    source_list = []
    target_list = []
    interaction_list = []

    # Extract data from JSON
    for entry in extracted_results:
        combined_results = entry.get('Combined_Results', []) 
        # Skip processing if the combined_results list is empty
        if not combined_results:
            continue
        for result in combined_results:
            if isinstance(result, str):  # Ensure the result is a string before attempting to split
                parts = result.split()
                if len(parts) == 3:
                    source, interaction, target = parts
                    source_list.append(source)
                    target_list.append(target)
                    interaction_list.append(interaction)

    # Create a DataFrame
    df = pd.DataFrame({
        'source': source_list,
        'target': target_list,
        'interaction': interaction_list
    })
    # print(df)

    factory = PandasDataFrameToCX2NetworkFactory()
    cx2_network = factory.get_cx2network(df, source_field='source', target_field='target', 
                                         edge_interaction='interaction')
    return cx2_network


if __name__ == "main":
    with open('results/pmc3898398/llm_combined50_results.json', 'r') as file:
        json_data = json.load(file)
    cx2_network = convert_to_cx2(json_data)
    cx2_network.set_name('Indra_50_sentences_network')
    net_cx = cx2_network.to_cx2()

    # Create an NDEx client instance with your credentials
    # client = Ndex2(username='favour.ujames196@gmail.com', password='Fujames17')
    # client.save_new_cx2_network(net_cx)

    # new_network = json.dumps(cx2_network.to_cx2(), indent=2)
    # with open('cx2.cx', 'w') as file:
    #     file.write(new_network)
