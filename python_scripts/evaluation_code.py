import json


def load_json_data(filepath):
    """Load JSON data from a file."""
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


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


# Extract the combined results for scoring
llm_predictions = []
indra_observations = []

llm_combined_results = load_json_data('results/pmc3898398/grounded_llm_results.json')
indra_combined_results = load_json_data('results/pmc3898398/indra_combined_results.json')
for llm_result, indra_result in zip(llm_combined_results, indra_combined_results):
    llm_predictions.extend(llm_result["Combined_Results"])
    indra_observations.extend(indra_result["Combined_Results"])
# Calculate scores
precision, recall, f1 = score(indra_observations, llm_predictions, verbose=True)
