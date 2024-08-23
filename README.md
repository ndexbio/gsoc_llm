# Large Language Model-based creation of knowledge graph from a publication
This goal of this project is to develop a Python web application that utilizes Large Language Models (LLMs) for extracting, transforming, and visualizing molecular interaction networks from scientific literature. This project is leveraging LLMs' advanced natural language processing capabilities, the application will interpret complex academic texts to construct interaction graphs. These results would be uploaded to the Network Data Exchange (NDEx) platform, enabling researchers to manage and visualize biological data more effectively. Key deliverables include: 
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
   
8. Utilized Gilda grounding service to ground the genes that are involved in the interactions that were gotten using the LLM in order to get better evaluation results.       
   `python_scripts/grounding_genes.py`

# Project Current State
1. Sentence_level extraction and comparison tasks were performed on the paper with PMCID:pmc3898398

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
   c. For ungrounded llm results(for 50 sentences), the scores gotten was:
   ```
   Final Score:
   Precision (micro): 39.22%
      Recall (micro): 42.55%
         F1 (micro): 40.82%
   ```
   d. For ungrounded llm results(for the whole paper), the scores gotten was:
   ```
   Final Score:
   Precision (micro): 18.52%
      Recall (micro): 23.65%
         F1 (micro): 20.77%
   ```
   
2. Processing time for the whole paper:

   a. With the Indra reach api: < 6 minutes
   
   b. With the OpenAI API: < 5 minutes

3. Best Performing prompt at the moment is: `papers/prompt_file_v3.txt`

4. Some examples of the interactions gotten are shown below:
   - Same interactions gotten for both indra and llm:
     <img width="881" alt="Screenshot 2024-08-24 at 00 30 46" src="https://github.com/user-attachments/assets/06115bf8-9047-49cf-8782-1089cd4bc307">
     <img width="875" alt="Screenshot 2024-08-24 at 00 31 04" src="https://github.com/user-attachments/assets/fb2c1bb0-7a3b-45ab-bc24-5b9082e80a7a">
   - Different interactions extracted from the same sentence where the LLM was more correct than the Indra Reach. In the example below, the LLM extracted several plausible biological interactions (such as "CLOCK RegulateAmount PER3", "PER1 Inhibition CLOCK", "CRY1 Inhibition BMAL1", etc.) that, while possible within the context of circadian rhythm biology, were not directly mentioned in the provided sentence. These inferred interactions suggest that the LLM is leveraging background biological knowledge to generate possible interactions that could be relevant in a broader biological context.
     <img width="879" alt="Screenshot 2024-08-24 at 00 35 10" src="https://github.com/user-attachments/assets/71cb0686-d551-4f7c-8342-19e9c0a9f6c1">
   - In the example below, The LLM correctly identifies both interactions mentioned in the sentence: the regulation by p53 of miRNA-34 and the subsequent decrease in SIRT1 expression by miRNA-34. INDRA's output does not capture the interactions described in the sentence. Instead, it suggests a self-inhibitory action by SIRT1 on itself, which is not relevant to the given text.
     <img width="925" alt="Screenshot 2024-08-24 at 00 39 18" src="https://github.com/user-attachments/assets/a30ce00c-014f-4993-b145-2eb4450f3a1c">
   - Example where the LLM did not extract correct interactions while the Indra reach extracted it correctly:
     
    
     



   

# Future Tasks
- Convert extracted interactions to CX2 networks and load the networks to cytoscape for visualisation
  
- Upload networks to NDEX from cytoscape
  
- Develop a tool(e.g web app) to enable a user upload scientific papers, get the interactions, and automatically upload the networks to NDEX and interact with the knowledgre graphs
  
- Testing out the model with other API like Claude 3.5 sonnet
  
- Perform prompt engineering techniques to get the most efficient prompt

# Challenges and Lessons Learned
## Lessons Learned
1. Advanced Prompt Engineering: Gained expertise in crafting detailed, efficient, and specific prompts for Large Language Models (LLMs) to optimize model interaction and enhance response accuracy.

2. API Integration and Usage: Developed proficiency in interfacing with the OpenAI API and INDRA Reach API, including making effective API calls and handling the responses for extracting biological interactions.

3. Schema Definition with Pydantic: Learned to utilize Pydantic functions to define robust model schemas, ensuring data validation and transformation into acceptable formats, particularly when integrating with LangChain for seamless data processing and model interaction.

4. Building Extraction Chains with LangChain: Mastered the use of LangChain to construct extraction chains, enabling complex multi-step reasoning processes and chained API calls. This included leveraging LangChain's capabilities to orchestrate API interactions for enriched data extraction workflows.

5. Modular Code Organization and GitHub Best Practices: Enhanced understanding of modularity and file organization within a GitHub repository to ensure maintainability, readability, and scalability of the project codebase.

6. Biological Interaction Types and Gene Grounding: Acquired knowledge on the various types of molecular interactions that occur between genes, as characterized by INDRA, and the importance of gene grounding. Learned techniques for ensuring accurate grounding of genes to improve data reliability and consistency.

7. Enhanced Understanding of Gene Grounding: Explored the concept of gene grounding in detail, focusing on techniques to ensure correct mapping and standardization of gene names across different databases and ontologies, crucial for accurate biological data interpretation.
  
## Challenges Faced
1. Installation of INDRA Reach API Locally:

   - Initially attempted to install the INDRA Reach API using Docker but encountered multiple issues related to Docker setup and execution.
   - Subsequently, attempted to utilize the NRNB cluster for the SBT method as per the Reach documentation, but this approach also proved unsuccessful.
   - Ultimately, resolved the issue by directly downloading and installing the INDRA Reach API using the SBT method on the local system.
     
2. Challenges in Comparing Results Between INDRA and LLM:

- The initial strategy of comparing results between INDRA and the LLM at a chunking level proved ineffective. This approach did not facilitate a meaningful comparison due to the variability in extracted text segments.
- An attempt was made to convert the entire document into sentences before passing them to the LLM and comparing the output with INDRA's results. However, this method failed because it performed word-by-word comparisons between sentences that were not identical in content and structure, leading to mismatched outputs.
- The solution involved shifting to a sentence-level extraction approach. Each sentence was processed individually, ensuring the order was maintained in a list. The same list of sentences was then passed to both the LLM and INDRA, allowing for a consistent comparison based on sentence index. This method ensured alignment in the processing order and facilitated a more accurate comparison of interactions extracted from both systems.
- Further steps included converting the output structures into a unified format, merging results into a single file for comprehensive analysis, and enabling easier manual comparison of the outputs from INDRA and the LLM.



# References
- https://cookbook.openai.com/
- https://indra.readthedocs.io/en/latest/modules/sources/reach/index.html
- https://platform.openai.com/docs/guides/prompt-engineering
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/
- https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/

