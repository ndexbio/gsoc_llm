# Large Language Model-based creation of knowledge graph from a publication
This project proposes the development of a Python web application that utilizes Large Language Models (LLMs) for extracting, transforming, and visualizing molecular interaction networks from scientific literature. This project is leveraging LLMs' advanced natural language processing capabilities, the application will interpret complex academic texts to construct interaction graphs. These results would be uploaded to the Network Data Exchange (NDEx) platform, enabling researchers to manage and visualize biological data more effectively. Key deliverables include: 
1. An interactive Python web app for document processing and extraction of interactions using LLMs.
2. Benchmarking of results gotten from LLM with results gotten from other sources to evaluate the performance of the LLM.
3. Seamless integration with the NDEx API for data management and graph visualization using Cytoscape.

## Prerequisites
Python (version 3.6 or higher)

## Installation
1. Clone this repo using:
   ```
   git clone (https://github.com/ndexbio/gsoc_llm) <folder_name>
   cd /<folder_name>
   ```
2. Create a virtual environment and activate it. Replace `myenv` with your desired name:
   ```
   conda create -n myenv python=3.8.0
   conda activate myenv
   ```
3. Install dependencies using: ``` pip install -r requirements.txt ```

   
## Extraction and Evaluation Task
To perform the task of extracting interactions from any scientific paper, in this case, the scientific paper with PMCID `pmc3898398`, follow the steps listed below:

1. Run the first script to prepare the model: `python python_scripts/model.py`
2. Next, run the interaction extraction script: `python python_scripts/get_interactions.py`
3. Then, run the sentence_level comparison script: `python_scripts/sentence_level_comparison.py`
5. Finally, to perform evaluation using indra, run the evaluation code script: `python_scripts/evaluation_code.py`

# Work Done
1. A model was created 

# Project Current State

# Future Tasks

# Challenges and Lessons Learned

# References

