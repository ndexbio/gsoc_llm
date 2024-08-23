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
3. Then, run the sentence_level comparison script: `python python_scripts/sentence_level_extraction.py`
5. Finally, to perform evaluation using indra, run the evaluation code script: `python python_scripts/evaluation_code.py`

# Work Done
1. Utilizing Pre-trained Models and APIs:
   a. Leveraged OpenAI API to develop LLM model for extracting complex biological interactions from scientific texts.
   b. Made use of LangChain to efficiently perform extraction tasks by integrating with advanced OpenAI models including gpt-3.5-turbo, gpt-4, gpt-4o, and gpt-4-Turbo.
   c. Created detailed model schematics using Pydantic functions, enhancing the structure and validation of data models used in the project: `python_scripts/model.py`
2. Perfromed prompt engineering to get the most efficient prompt. There are 3 versions of the prompt as seen under the `papers` folder
3. Developed the get interactions script: `python_scripts/get_interactions.py`.
   This script is responsible for reading in the prompt and running the extraction chain. The extraction chain was created using Langchain tools.
   The extraction chain flows this way:
   prompt ----> extraction_model ----> Json_output_parser
5. Interacting with Indra Reach:
   a. Downloaded and installed Indra Reach API locally
   b. Utilized INDRA REACH to retrieve INDRA statements from PMCIDs: `python_scripts/get_indra_statements.py`
   c. Wrote code to get PMCIDs of papers that have PMIDs easily available: `python_scripts/get_pmcid.py`
6. Chunking_level Extraction: `python_scripts/chunking_level_extraction.py`
   Implemented text chunking strategies to prepare large texts for processing through large language models (LLMs), facilitating the extraction of molecular interactions from segmented    text. This was done using Langchain's textsplitter function.
7. Sentence_level Extraction: `python_scripts/sentence_level_extraction.py`
   a. Applied sentence-level extraction techniques to scientific documents using OpenAI API and INDRA REACH API to obtain precise interaction data. This was done by processing the            statements gotten from indra to get only the sentences.
   b. This ensured that the same set of sentences were passed through the LLM first, then the indra reach api for processing sentence by sentence. Then the sentence, and the results          from each of the API was noted.
8. Comparison and Evaluations:
   a. Modified the structure of the results gotten from both the indra reach and LLM to prepare it for evaluation as seen in the functions defined in the script,       
      `python_scripts/sentence_level_extraction.py`:
   ```
   combine_interaction
   create_combined_results
   combine_llm_and_indra_results
   ```
   b. Wrote code to compare the extracted interactions from both APIs and used F1_score as the evaluation metric. `python_scripts/evaluation_code.py`
9. Utilized Gilda grounding service to ground the genes that are involved in the interactions that were gotten using the LLM. `python_scripts/grounding_genes.py`


# Project Current State

# Future Tasks

# Challenges and Lessons Learned

# References

