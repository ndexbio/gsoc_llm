import pandas as pd
import json
from ndex2.cx2 import PandasDataFrameToCX2NetworkFactory
from ndex2.client import Ndex2

# Load your JSON data from file
with open('results/pmc3898398/llm_combined50_results.json', 'r') as file:
    json_data = json.load(file)

# Initialize lists to store extracted data
source_list = []
target_list = []
interaction_list = []

# Extract data from JSON
for entry in json_data:
    combined_results = entry.get('Combined_Results', [])
    for result in combined_results:
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
cx2_network = factory.get_cx2network(df, source_field='source', target_field='target', edge_interaction='interaction')
# cx2_network.set_name('Set any name of your choice')

net_cx = cx2_network.to_cx2()
# Create an NDEx client instance with your credentials
client = Ndex2(username='favour.ujames196@gmail.com', password='Fujames17')
client.save_new_cx2_network(net_cx)


new_network = json.dumps(cx2_network.to_cx2(), indent=2)
with open('results/cx2.cx', 'w') as file:
    file.write(new_network)


