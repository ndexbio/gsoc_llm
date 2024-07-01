import json
import pandas as pd
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from get_indra_statements import convert_indra_to_langchain_format


# with open("/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/PMC6044858_indra.json", 'r') as file:
#     data = json.load(file)
#     interactions = convert_indra_to_langchain_format(data)


# def load_interactions(file_path):
#     """ Load interaction details from a JSON file. """
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#         detailed_interactions = [{
#             "subject": interaction.get("subject"),
#             "object": interaction.get("object"),
#             "interaction_type": interaction.get("interaction_type"),
#             "text": interaction.get("text")
#         } for interaction in data if "text" in interaction]
#     return detailed_interactions


def load_sentences_from_json(file_path):
    """ Load interaction details from a JSON file. """
    with open(file_path, 'r') as file:
        data = json.load(file)
        sentences = [interaction["text"] for interaction in data if "text" in interaction]
    return sentences


# Load sentences from both JSON files
sentences1 = load_sentences_from_json('/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/sentence_output_direct.json')
sentences2 = load_sentences_from_json('/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/conv_indra_results.json')

# Vectorize the sentences
vectorizer = TfidfVectorizer()
all_sentences = sentences1 + sentences2
all_sentence_vectors = vectorizer.fit_transform(all_sentences)

# Compare the vectors
similarity_matrix = cosine_similarity(all_sentence_vectors[:len(sentences1)], all_sentence_vectors[len(sentences1):])

results = []
for i, row in enumerate(similarity_matrix):
    best_match = row.argmax()
    best_match_score = row[best_match]
    results.append({
        "Sentence Index File 1": i,
        "Sentence in File 1": sentences1[i],
        "Sentence Index File 2": best_match,
        "Sentence in File 2": sentences2[best_match],
        "Similarity Score": best_match_score
    })

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(results)
print(df)
# print("Results have been saved to 'sentence_similarity_results.csv'")
