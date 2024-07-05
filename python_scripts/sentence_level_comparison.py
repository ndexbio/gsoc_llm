import json
from get_interactions import extraction_chain
from indra.sources import reach
import time


file_path = '/Users/favourjames/Downloads/gsoc_llm/results/pmc3898398/indra_results.json'
with open(file_path, 'r') as file:
    data = json.load(file)


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


sentences = extract_sentences(data)
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

# # Save the LLM results to a JSON file
# with open('llm_results.json', 'w') as llm_file:
#     json.dump(llm_results, llm_file, indent=4)

# # Save the INDRA REACH results to a JSON file
# with open('indra_reach_results.json', 'w') as indra_file:
#     json.dump(indra_reach_results, indra_file, indent=4)

# print("LLM results have been saved to 'llm_results.json'.")
# print("INDRA REACH results have been saved to 'indra_reach_results.json'.")


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


def score(observations, predictions, verbose=False):
    correct_by_relation = 0
    predicted_by_relation = 0
    observed_by_relation = 0

    # Determine the counts of predicted and observed excluding empty strings
    tmp_predictions = [p for p in predictions if p != '']
    tmp_observations = [o for o in observations if o != '']

    predicted_by_relation += len(tmp_predictions)
    observed_by_relation += len(tmp_observations)

    # Loop over the predictions to find matching
    for row in range(len(tmp_predictions)):
        predicted = tmp_predictions[row]  
        if predicted in tmp_observations:
            correct_by_relation += 1

    # Print the aggregate score (micro-averaged since across all relations)
    prec_micro = 1.0
    if predicted_by_relation > 0:
        prec_micro = correct_by_relation / predicted_by_relation
    recall_micro = 0.0
    if observed_by_relation > 0:
        recall_micro = correct_by_relation / observed_by_relation
    f1_micro = 0.0
    if prec_micro + recall_micro > 0.0:
        f1_micro = 2.0 * prec_micro * recall_micro / (prec_micro + recall_micro)
    if verbose:
        print("Final Score:")
        print("Precision (micro): {:.2%}".format(prec_micro))
        print("   Recall (micro): {:.2%}".format(recall_micro))
        print("       F1 (micro): {:.2%}".format(f1_micro))

    return round(prec_micro, 3), round(recall_micro, 3), round(f1_micro, 3)


# Extract the combined results for scoring
llm_predictions = []
indra_observations = []

for llm_result, indra_result in zip(llm_combined_results, indra_combined_results):
    llm_predictions.extend(llm_result["Combined_Results"])
    indra_observations.extend(indra_result["Combined_Results"])

# Calculate scores
precision, recall, f1 = score(indra_observations, llm_predictions, verbose=True)


def jaccard_similarity(text1, text2):
    # Ensure inputs are strings
    if not isinstance(text1, str):
        text1 = str(text1)
    if not isinstance(text2, str):
        text2 = str(text2)      
    # Tokenize the texts into sets of words
    set1 = set(text1.split())
    set2 = set(text2.split())
    # Calculate the intersection and union of the two sets
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    # Compute the Jaccard similarity
    if not union:
        return 0.0
    return len(intersection) / len(union)
