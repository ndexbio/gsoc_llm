import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from model import extraction_model
warnings.filterwarnings("ignore")


def get_prompt(identifier, filepath):
    with open(filepath, 'rb') as file:
        content = file.read()
    # Check for BOM and remove it
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]

    lines = content.decode('utf-8').splitlines()
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
filepath = 'papers/prompt_file_v3.txt'
prompt_identifier = 'general prompt'
prompt = get_prompt(prompt_identifier, filepath)
# print(prompt)


# Define the extraction chain
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="interactions")
