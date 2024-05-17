import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from model import extraction_model
warnings.filterwarnings("ignore")

# Write a prompt for extracting molecular interactions
template = """A scientific paper will be provided to you. 
Ensure to extract all molecular interactions mentioned in this paper.
Identify the entities involved in each interaction and describe the type of interaction
(e.g., binding, inhibition, activation).
If detailed interaction mechanisms or effects are mentioned, include those as well.
Do not include any background information or general knowledge not directly 
related to the interactions described in the paper.
Only extract and report on the specific molecular interactions that the paper presents."""

# Define the extraction chain
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="interactions")
