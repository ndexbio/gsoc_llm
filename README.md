# GSoC_LLM Project
This project proposes the development of a Python web application that utilizes Large Language Models (LLMs) for extracting, transforming, and visualizing molecular interaction networks from scientific literature. This project is leveraging LLMs' advanced natural language processing capabilities, the application will interpret complex academic texts to construct interaction graphs. These results would be uploaded to the Network Data Exchange (NDEx) platform, enabling researchers to manage and visualize biological data more effectively.

## Prerequisites
Python (version 3.6 or higher)

## Installation
1. Clone this repo using:
   ```
   git clone (https://github.com/ndexbio/gsoc_llm) <folder_name>
   cd /<folder_name>
   ```
3. Install dependencies using: ```pip install -r requirements.txt```
   
## Extraction Task
To perform the task of extracting interactions from the scientific paper, follow the steps listed below:

1. Run the first script to prepare the model
  
3. Next, run this script: python_scripts/get_interactions.py
4. Then, run this script: python_scripts/sentence_level_comparison.py

