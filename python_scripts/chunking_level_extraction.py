import json
import time
from get_interactions import extraction_chain
from indra_nxml_extraction import extract_text, get_xml_from_file
# import spacy
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda


# Start the timer
start_time = time.time()


xml_string = get_xml_from_file("/Users/favourjames/Downloads/gsoc_llm/results/pmc6044858/output.xml")
text = extract_text(xml_string)


# Define a function to flatten a 2D list (matrix) into a 1D list (flat list).
def flatten(matrix):
    flat_list = []
    # Iterate through each row in the 2D list.
    for row in matrix:
        flat_list += row
    return flat_list


text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)
splits = text_splitter.split_text(text)

prep = RunnableLambda(
    lambda x: [{"input": doc} for doc in text_splitter.split_text(x)]
)

chain = prep | extraction_chain.map() | flatten
results = chain.invoke(text)


json_output = json.dumps(results, indent=4)
with open('results/pmc6044858/output.json', 'w') as file:
    file.write(json_output)


end_time = time.time()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60
print(f"Time taken: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")


# to process the document by sentences
# nlp = spacy.load("en_core_web_sm")
# doc = nlp(text)
# sentences = []
# for sent in doc.sents:
#     if "Supporting information" in sent.text:
#         break
#     # sentences += sent.text + " "
#     sentences.append(sent.text)

# sentences = sentences[:100]
# prep = RunnableLambda(
#     lambda x: [{"input": sentence} for sentence in sentences]
# )
