import json
from get_interactions import extraction_chain
from indra.sources import reach
import time
# from grounding_genes import ground_genes


def load_json_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


file_path = 'results/pmc3898398/indra_results.json'
indra_data = load_json_data(file_path)


def extract_sentences(data):
    sentences = {}
    index = 0  # Initialize a counter to keep track of the indices
    for item in data:
        if 'evidence' in item:
            for evidence in item['evidence']:
                if 'text' in evidence:
                    sentences[str(index)] = evidence['text']
                    index += 1  # Increment the index for each sentence
    return sentences


sentences = extract_sentences(indra_data)
#get 50 random sentences for comparison prototype
selected_keys = sorted(sentences.keys())[:]

# Initialize dictionaries to store the results
llm_results = {}
indra_reach_results = {}

#extracting interactions from each sentence using llm
llm_results["LLM_extractions"] = []
start_time = time.time()
for index in selected_keys:
    sentence = sentences[index]
    results = extraction_chain.invoke({"input": sentence})
    llm_results["LLM_extractions"].append({
        "Index": index,
        "Sentence": sentence,
        "Results": results
    })
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60
print(f"Time taken: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")

with open('results/llm_results.json', 'w') as llm_file:
    json.dump(llm_results, llm_file, indent=4)

# perform extraction using indra reach
indra_reach_results["INDRA_REACH_extractions"] = []
start_time = time.time()
for index in selected_keys:
    sentence = sentences[index]
    reach_processor = reach.api.process_text(sentence)
    stmts = reach_processor.statements
    statements_json = [stmt.to_json() for stmt in stmts]
    indra_reach_results["INDRA_REACH_extractions"].append({
        "Index": index,
        "Sentence": sentence,
        "Results": statements_json
    })
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60
print(f"Time taken for indra processing: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")

with open('results/indra_results.json', 'w') as indra_file:
    json.dump(indra_reach_results, indra_file, indent=4)


#function to create sub-interaction type-obj
def combine_interaction(interaction):
    if 'subject' in interaction and 'object' in interaction:
        return f"{interaction['subject']} {interaction['interaction_type']} {interaction['object']}"
    elif 'enz' in interaction and 'sub' in interaction:
        return f"{interaction['enz']['name']} {interaction['type']} {interaction['sub']['name']}"
    elif 'subj' in interaction and 'obj' in interaction:
        return f"{interaction['subj']['name']} {interaction['type']} {interaction['obj']['name']}"
    elif 'members' in interaction and len(interaction['members']) == 2:
        member1, member2 = interaction['members']
        return f"{member1['name']} {interaction['type']} {member2['name']}"
    else:  # Handle unexpected formats
        return None, None, None


# Create combined results
def create_combined_results(results):
    combined_results = []
    for result in results:
        combined_entry = {
            "Index": result["Index"],
            "Sentence": result["Sentence"],
            "Combined_Results": list(set([combine_interaction(interaction) for interaction in result["Results"]]))
        }
        combined_results.append(combined_entry)
    return combined_results


llm_combined_results = create_combined_results(llm_results["LLM_extractions"])
indra_combined_results = create_combined_results(indra_reach_results["INDRA_REACH_extractions"])

# Save the results to different JSON files
with open('indra_combined_results.json', 'w') as indra_file:
    json.dump(indra_combined_results, indra_file, indent=4)

with open('llm_combined_results.json', 'w') as outfile:
    json.dump(llm_combined_results, outfile, indent=4)


#function to save both indra outputs and llm outputs in one file
def combine_llm_and_indra_results(llm_filepath, indra_filepath):
    llm_results = load_json_data(llm_filepath)
    indra_results = load_json_data(indra_filepath)
    combined_data = []

    # Create a dictionary to match entries by index
    llm_dict = {entry["Index"]: entry for entry in llm_results}
    indra_dict = {entry["Index"]: entry for entry in indra_results}

    # Get all unique indices from both LLM and INDRA results
    all_indices = set(llm_dict.keys()).union(set(indra_dict.keys()))

    for index in all_indices:
        llm_entry = llm_dict.get(index, {"Sentence": "", "Combined_Results": []})
        indra_entry = indra_dict.get(index, {"Sentence": "", "Combined_Results": []})

        combined_entry = {
            "index": index,
            "sentence": llm_entry["Sentence"] or indra_entry["Sentence"],
            "llm": llm_entry["Combined_Results"],
            "indra": indra_entry["Combined_Results"]
        }
        combined_data.append(combined_entry)
    return combined_data


combined_data = combine_llm_and_indra_results('results/pmc3898398/llm_combined_results.json', 
                                              'results/pmc3898398/indra_combined_results.json')

# with open('results/pmc3898398/combined_output.json', 'w') as outfile:
#     json.dump(combined_data, outfile, indent=4)


# Define the function to ground genes in combined results
# def ground_genes_in_combined_results(combined_results):
#     for entry in combined_results:
#         interactions = entry["Combined_Results"]
#         if not interactions:  # Check if interactions list is empty
#         continue
#         genes = set()
#         for interaction in interactions:
#             parts = interaction.split()
#             if len(parts) == 3:
#                 genes.add(parts[0])
#                 genes.add(parts[2])
#         grounded_genes = ground_genes(list(genes))
#         grounded_interactions = []
#         for interaction in interactions:
#             parts = interaction.split()
#             if len(parts) == 3:
#                 grounded_subject = grounded_genes.get(parts[0], parts[0])
#                 grounded_object = grounded_genes.get(parts[2], parts[2])
#                 grounded_interactions.append(f"{grounded_subject} {parts[1]} {grounded_object}")
#         entry["Combined_Results"] = grounded_interactions
#     return combined_results


# grounded_llm_combined_results = ground_genes_in_combined_results(llm_combined_results)

# with open('results/pmc3898398/grounded_llm_results.json', 'w') as outfile:
#     json.dump(grounded_llm_combined_results, outfile, indent=4)
