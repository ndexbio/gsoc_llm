import os
import json
import requests

# Define the grounding service URL
os.environ["INDRA_DB_REST_URL"] = "https://db.indra.bio"
grounding_service_url = 'http://grounding.indra.bio/ground'


def load_json_data(filepath):
    """Load JSON data from a file."""
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


def extract_genes(data):
    """Extract unique genes from the list of interactions."""
    genes = set()
    for interaction in data:
        genes.add(interaction['subject'])
        genes.add(interaction['object'])
    return list(genes)


def ground_genes(genes):
    """Ground a list of gene names using the grounding service."""
    grounded_genes = {}
    for gene in genes:
        response = requests.post(grounding_service_url, json={'text': gene})
        if response.status_code == 200:
            results = response.json()
            if results:
                grounded_genes[gene] = results[0]['term']['id'] + '@' + results[0]['term']['db']
            else:
                grounded_genes[gene] = None
        else:
            grounded_genes[gene] = None
    return grounded_genes


# interactions = load_json_data('/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/sentence_output.json')

# genes = extract_genes(interactions)

# grounded_genes = ground_genes(genes)

# #Save the grounded genes
# json_output = json.dumps(grounded_genes, indent=4)
# with open('results/pmc333362/grounded_genes', 'w') as file:
#     file.write(json_output)
