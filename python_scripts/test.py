import json
import time
from get_interactions import extraction_chain
from indra_nxml_extraction import extract_text, get_xml_from_file
from langchain.schema.runnable import RunnableLambda


class extract_sentences(BaseModel):
    """sentences to extract"""
    sentences: List[str] = Field(..., description="Any sentence that contains at least two genes interacting \
        with each other in one way or the other")
    
    
sentence_model = model.bind(
    functions=sentence_extraction_function,
    # function_call={"name": "DocumentInteractions"}
)

# Convert the pydantic classes to openai model
sentence_extraction_function = [
    convert_pydantic_to_openai_function(extract_sentences)   
]
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


sentences = sentence_chain.invoke(text)
print(sentences)

sent_template = """ Extract every sentence that contains at least two entities/genes interacting with one another. The 
results that should be gotten from this prompt should look like this:
"Nonstructural protein 1 (NS1) of dengue virus (DENV) can stimulate endothelial cells to secrete endothelial 
hyperpermeability factor, macrophage migration inhibitory factor (MIF), and the glycocalyx degradation factor 
heparanase 1 (HPA-1)." Another sample is "DENV NS1 may bind to the TLR4 of leukocytes, inducing the secretion of 
cytokines and MMPs, or it may directly bind to endothelial cells, inducing the secretion of HPA-1, both of which can 
cause glycocalyx degradation and subsequent vascular leakage." Then another sample is "Activated HPA-1 enhances 
shedding of the transmembrane heparan sulfate proteoglycan syndecan-1 (CD138) and elevates the level of CD138 in the 
bloodstream [7, 9, 10]."
"""


# # Prepare the text for the extraction chain
# prep = RunnableLambda(
#     lambda x: [{"input": sentence} for sentence in sentences]
# )

# chain = prep | extraction_chain.map() | flatten
# results = chain.invoke(text)

# json_output = json.dumps(results, indent=4)
# with open('results/pmc6044858/sentence_output.json', 'w') as file:
#     file.write(json_output)

# end_time = time.time()
# elapsed_time = end_time - start_time
# elapsed_minutes = elapsed_time / 60
# print(f"Time taken: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")

