import json
from get_interactions import extraction_chain
import time


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
selected_keys = sorted(sentences.keys())[:50]

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
# print(f"Index: {index}, Sentence: '{sentence}', Results: {results}")

#perform extraction using indra reach
# indra_reach_results["INDRA_REACH_extractions"] = []
# start_time = time.time()
# for index in selected_keys:
#     sentence = sentences[index]
#     reach_processor = reach.api.process_text(sentence)
#     stmts = reach_processor.statements
#     statements_json = [stmt.to_json() for stmt in stmts]
#     indra_reach_results["INDRA_REACH_extractions"].append({
#         "Index": index,
#         "Sentence": sentence,
#         "Results": statements_json
#     })
# end_time = time.time()
# elapsed_time = end_time - start_time
# elapsed_minutes = elapsed_time / 60
# print(f"Time taken for indra processing: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")

# Save the LLM results to a JSON file
# with open('llm_results.json', 'w') as llm_file:
#     json.dump(llm_results, llm_file, indent=4)

# Save the INDRA REACH results to a JSON file
# with open('indra_reach_results.json', 'w') as indra_file:
#     json.dump(indra_reach_results, indra_file, indent=4)


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
