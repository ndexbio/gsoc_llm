import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_sentences_from_json(file_path):
    """ Load interaction details from a JSON file. """
    with open(file_path, 'r') as file:
        data = json.load(file)
        sentences = [interaction["text"] for interaction in data if "text" in interaction]
    return sentences


# Load sentences from both JSON files
sentences1 = load_sentences_from_json('/Users/favourjames/Downloads/gsoc_llm/results/pmc333362/conv_indra_results.json')
sentences2 = load_sentences_from_json('/Users/favourjames/Downloads/gsoc_llm/results/pmc333362/output_4o.json')

# Vectorize the sentences
vectorizer = TfidfVectorizer()
all_sentences = sentences1 + sentences2
all_sentence_vectors = vectorizer.fit_transform(all_sentences)

# Compare the vectors
similarity_matrix = cosine_similarity(all_sentence_vectors[:len(sentences1)], all_sentence_vectors[len(sentences1):])

# Process the similarity matrix to find the best matches
for i, row in enumerate(similarity_matrix):
    best_match = row.argmax()
    print(f"Sentence {i} in file 1 is most similar to Sentence {best_match}\
          in file 2 with similarity score: {row[best_match]}")
