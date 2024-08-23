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

4. Finally, to perform evaluation using indra, run the evaluation code script: `python python_scripts/evaluation_code.py`

# Work Done
1. Utilizing Pre-trained Models and APIs:
   
   a. Leveraged OpenAI API to develop LLM model for extracting complex biological interactions from scientific texts.
   
   b. Made use of LangChain to efficiently perform extraction tasks by integrating with advanced OpenAI models including gpt-3.5-turbo, gpt-4, gpt-4o, and gpt-4-Turbo.
   
   c. Created detailed model schematics using Pydantic functions, enhancing the structure and validation of data models used in the project: `python_scripts/model.py`
   
2. Perfromed prompt engineering to get the most efficient prompt. There are 3 versions of the prompt as seen under the `papers` folder
   
3. Developed the get interactions script: `python_scripts/get_interactions.py`.
   
   This script is responsible for reading in the prompt and running the extraction chain. The extraction chain was created using Langchain tools.
   
   The extraction chain flows this way: prompt ----> extraction_model ----> Json_output_parser
4. Interacting with Indra Reach:
   
   a. Downloaded and installed Indra Reach API locally
   
   b. Utilized INDRA REACH to retrieve INDRA statements from PMCIDs: `python_scripts/get_indra_statements.py`
   
   c. Wrote code to get PMCIDs of papers that have PMIDs easily available: `python_scripts/get_pmcid.py`
   
5. Chunking_level Extraction: `python_scripts/chunking_level_extraction.py`
   
   Implemented text chunking strategies to prepare large texts for processing through large language models (LLMs), facilitating the extraction of molecular interactions from segmented
   text. This was done using Langchain's textsplitter function.
   
6. Sentence_level Extraction: `python_scripts/sentence_level_extraction.py`
   
   a. Applied sentence-level extraction techniques to scientific documents using OpenAI API and INDRA REACH API to obtain precise interaction data. This was done by processing the            statements gotten from indra to get only the sentences.
   
   b. This ensured that the same set of sentences were passed through the LLM first, then the indra reach api for processing sentence by sentence. Then the sentence, and the results          from each of the API was noted.
   
7. Comparison and Evaluations:
   
   a. Modified the structure of the results gotten from both the indra reach and LLM to prepare it for evaluation as seen in the functions defined in the script,       
      `python_scripts/sentence_level_extraction.py`:
   ```
   combine_interaction
   create_combined_results
   combine_llm_and_indra_results
   ```
   b. Wrote code to compare the extracted interactions from both APIs and used F1_score as the evaluation metric. `python_scripts/evaluation_code.py`
   
8. Utilized Gilda grounding service to ground the genes that are involved in the interactions that were gotten using the LLM. `python_scripts/grounding_genes.py`

# Project Current State
1. Sentence_level extraction and comparison tasks were performed on the paperwith PMCID:pmc3898398

   a. For 50 sentences from the paper, the scores gotten was:
   ```
   Final Score:
   Precision (micro): 46.94%
      Recall (micro): 48.94%
         F1 (micro): 47.92%
   ```
   b. For all the sentences in the paper, the scores gotten was:
   ```
   Final Score:
   Precision (micro): 25.41%
      Recall (micro): 31.08%
         F1 (micro): 27.96%
   ```
2. Processing time for the whole paper:

   a. With the Indra reach api: < 6 minutes
   
   b. With the OpenAI API: < 5 minutes

3. Best Performing prompt at the moment is: `papers/prompt_file_v3.txt`
   

# Future Tasks
- Convert extracted interactions to CX2 networks and load the networks to cytoscape for visualisation
  
- Upload networks to NDEX from cytoscape
  
- Develop a tool(e.g web app) to enable a user upload scientific papers, get the interactions, and automatically upload the networks to NDEX and interact with the knowledgre graphs
  
- Testing out the model with other API like Claude 3.5 sonnet
  
- Perform prompt engineering techniques to get the most efficient prompt

# Challenges and Lessons Learned
## Lessons Learned
- Developed skills in crafting well-detailed, efficient, and specific prompts for LLMs, optimizing the interaction and response accuracy of the models.

- Learnt how to interact with OpenAI API and Indra Reach API.
  
- I learnt how to create use pydantic functions to define model schemas and convert them to acceptable format using Langchain
  
- I learnt how to use Langchain to build extraction chains, in order to make chain calls and also how to use it to interact with APIs
  
- I learnt about modularity and organisation of files on GitHub
  
- I learnt about the different interaction types that are possible between genes based on indra
  
- I learnt about what grounding of genes and how to ensure your genes are grounded
  
## Challenges Faced
1. Downloading and installing the Indra Reach API locally
   
   a. First, tried the docker way but got issues with using docker
   
   b. Tried using NRNB cluster to use the sbt method as described on the Reach documentation but it also did not work out
   
   c. Ended up using the sbt download method on my local system
   
2. Faced challenges when trying to perform comparison between the results gotten from indra and the one from the LLM
   
   a. This could not be done with the results gotten by chunking_level extractions
   
   b. I tried to convert the whole document to sentence first, before parsing it to the llm, then comparing the results gotten from the llm and the indra. However, since comparison of       text is done word by word, this approach did not work because it was not the same sentence that was sent, so the arrangement of the results gotten from the indra and the llm           differed. This made it extremely difficult to perform comparison
   
   c. To solve this issue, my mentors suggested making performing sentence_level extractions, such that I would take note of the sentences being parsed and ensure it is arranged accordingly in a list, then send the sentence one by one to the llm. After which, I send the same list of sentences to the indra. This way, the index of each of the sentence was noted, and we could know which sentence was processed and see the interactions gotten from the llm and the indra.
   
   d. Further processing included converting the structures of the output, joining the output together to observe the different results gotten in one file, before proceeding to perform evaluation. This also makes it easier for the results to be compared manually.



# References
- https://cookbook.openai.com/
- https://indra.readthedocs.io/en/latest/modules/sources/reach/index.html
- https://platform.openai.com/docs/guides/prompt-engineering
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/
- https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/

