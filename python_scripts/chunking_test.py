import json
import time
from read_pdf import read_pdf
from get_interactions import extraction_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda


# Start the timer
start_time = time.time()

doc = read_pdf("/Users/favourjames/Downloads/gsoc_llm/papers/review_paper1.pdf")
page_content = doc


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
# print(splits[0])
# print(len(splits[0]))
# print(len(splits))


chain = prep | extraction_chain.map() | flatten
results = chain.invoke(page_content)

# Count the number of interactions
interaction_count = len(results)
print(f"Number of interactions: {interaction_count}")

# Initialize a set to store unique interaction types
unique_interaction_types = set()
for interaction in results:
    if 'interaction_type' in interaction:
        unique_interaction_types.add(interaction['interaction_type'])
print(f"Number of unique interaction types: {len(unique_interaction_types)}")


json_output = json.dumps(results, indent=4)
with open('results/SIRT1_PARP1/output3.json', 'w') as file:
    file.write(json_output)


end_time = time.time()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60
print(f"Time taken: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")
