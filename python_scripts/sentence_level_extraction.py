import time
from get_interactions import extraction_chain
from indra_nxml_extraction import extract_text, get_xml_from_file
import spacy
from langchain.schema.runnable import RunnableLambda


start_time = time.time()

# Define a function to extract text from XML
xml_string = get_xml_from_file("/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/output.xml")
text = extract_text(xml_string)


# Define a function to flatten a 2D list (matrix) into a 1D list (flat list).
def flatten(matrix):
    flat_list = []
    # Iterate through each row in the 2D list.
    for row in matrix:
        flat_list += row
    return flat_list


# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")


doc = nlp(text)
sentences = []
for sent in doc.sents:
    if "Supporting information" in sent.text:
        break
    # sentences += sent.text + " "
    sentences.append(sent.text)

sentences = sentences[:100]
# print(len(sentences))


# Prepare the text for the extraction chain
prep = RunnableLambda(
    lambda x: [{"input": sentence} for sentence in sentences]
)

chain = prep | extraction_chain.map() | flatten
results = chain.invoke(text)


end_time = time.time()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60
print(f"Time taken: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")
