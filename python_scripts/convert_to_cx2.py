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
        for entity in interaction['entities_involved']:
            if entity not in nodes_map:
                nodes_map[entity] = node_id
                cx2_network['nodes'].append({"@id": node_id, "n": entity})
                node_id += 1

        source_node_id = nodes_map[interaction['entities_involved'][0]]
        target_node_id = nodes_map[interaction['entities_involved'][1]]

        # Add edge based on the interaction
        cx2_network['edges'].append({"@id": edge_id, "s": source_node_id, "t": target_node_id, 
                                     "i": interaction['interaction_type']})
        edge_id += 1

        # Optionally, add edge attributes if interaction_details are present
        if interaction.get('interaction_details'):
            cx2_network['edgeAttributes'].append({
                "po": edge_id - 1,          
                "n": "interaction_details",
                "v": interaction['interaction_details']
            })

    return cx2_network
