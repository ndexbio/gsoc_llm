from read_pdf import read_pdf
import json
from get_interactions import extraction_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda

doc = read_pdf("/Users/favourjames/Downloads/gsoc_llm/papers/review_paper1.pdf")
page_content = doc[50:50000]


# Define a function to flatten a 2D list (matrix) into a 1D list (flat list).
def flatten(matrix):
    flat_list = []
    # Iterate through each row in the 2D list.
    for row in matrix:
        flat_list += row
    return flat_list


text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)
splits = text_splitter.split_text(page_content)

prep = RunnableLambda(
    lambda x: [{"input": doc} for doc in text_splitter.split_text(x)]
)

chain = prep | extraction_chain.map() | flatten

results = chain.invoke(page_content)
json_output = json.dumps(results, indent=4)
print(json_output)
