import json


def convert_to_cx2(extracted_data):
    # Initialize the CX2 format structure
    cx2_network = {
        "nodes": [],
        "edges": [],
        "networkAttributes": [],
        "nodeAttributes": [],
        "edgeAttributes": []
    }
    # Define node and edge ids
    node_id = 1
    edge_id = 1

    # Maps to keep track of nodes and ensure they're unique
    nodes_map = {}

    # Process each interaction
    for interaction in extracted_data:
        for key in ['subject', 'object']:
            entity = interaction.get(key)
            if entity and entity not in nodes_map:
                nodes_map[entity] = node_id
                cx2_network['nodes'].append({"@id": node_id, "n": entity})
                node_id += 1

        # Add edge based on the interaction
        source_node_id = nodes_map.get(interaction['subject'])
        target_node_id = nodes_map.get(interaction['object'])
        cx2_network['edges'].append({
            "@id": edge_id, 
            "s": source_node_id, 
            "t": target_node_id,
            "i": interaction['interaction_type']
        })
        edge_id += 1

        # Optionally, add edge attributes if interaction details are present
        if interaction.get('text'):
            cx2_network['edgeAttributes'].append({
                "po": edge_id - 1,
                "n": "interaction_details",
                "v": interaction['text']
            })

    return cx2_network


file_path = '/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/sentence_output.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert extracted data to CX2 format
cx2_network = convert_to_cx2(data)

with open("results/pmc6044858/cx2_format.json", "w") as file:
    json.dump(cx2_network, file, indent=4)
