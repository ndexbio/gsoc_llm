import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from model import extraction_model
warnings.filterwarnings("ignore")


def get_prompt(identifier):
    with open('papers/prompt_file.txt', 'r') as file:
        lines = file.readlines()
        prompt = []
        capture = False
        for line in lines:
            if line.strip().startswith('#') and identifier in line:
                capture = True
                continue
            if capture:
                if line.strip().startswith('#') and len(prompt) > 0:
                    break
                prompt.append(line)
        return ''.join(prompt)


# Usage
prompt_identifier = 'general prompt'
prompt = get_prompt(prompt_identifier)
# print(prompt)


# Define the extraction chain
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="interactions")
