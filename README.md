# Large Language Model-based creation of knowledge graph from a publication
This goal of this project is to develop a Python web application that utilizes Large Language Models (LLMs) for extracting, transforming, and visualizing molecular interaction networks from scientific literature. This project is leveraging LLMs' advanced natural language processing capabilities, the application will interpret complex academic texts to construct knowledge graphs. These results would be uploaded to the Network Data Exchange (NDEx) platform, enabling researchers to manage and visualize biological data more effectively. 

Key deliverables include: 
1. An Interactive Web Extension for Cytoscape: Develop a web extension for the Cytoscape web application that facilitates document processing and interaction extraction using Large Language Models (LLMs). 
2. Benchmarking of Extraction Methods: Perform benchmarking to compare results from LLMs with those obtained using Indra Reach API. This comparison aims to evaluate the performance and accuracy of the LLMs in extracting biological interactions from text, providing insights into their effectiveness relative to established extraction tools.
3. Integration with NDEx for Network Management: Achieve seamless integration with the NDEx API for uploading CX2 networks and visualizing these networks in Cytoscape. NDEx (Network Data Exchange) is a platform that allows for the storage, sharing, and visualization of biological networks, enabling researchers to manage their data more effectively. This integration will ensure that the extracted networks are readily accessible for further analysis and interpretation and visualizations using Cytoscape, an open-source software platform specifically designed for visualizing complex networks and integrating these with any type of attribute data.

- INDRA (Integrated Network and Dynamical Reasoning Assembler) is a tool that automates the assembly of knowledge networks from natural language descriptions of biological processes. It provides a framework for integrating various sources of biological data, allowing for the construction of complex interaction networks.

- REACH (Reading and Assembling Contexts in High-throughput) is an information extraction system within INDRA that specifically focuses on identifying and extracting molecular interactions from scientific texts. 

### Brief description of Knowledge graphs
A knowledge graph is a structured representation of relationships between entities, like molecular interactions extracted from scientific literature. It enables intuitive querying, reasoning, and visualization of complex biological data, aiding in understanding biological systems and facilitating discoveries. 

The knowledge graph in this project will focus on representing molecular interactions, specifically focusing on relationships and other biological interactions described in the literature. This graph will include nodes representing biological entities (e.g., proteins, genes) and edges representing the interactions between these entities. 

### Why is a Knowledge Graph Helpful to Scientists? 
Knowledge graphs are valuable to scientists because they provide a comprehensive and easily navigable representation of complex relationships within biological data. They help in understanding how different molecules interact in a biological pathway, identifying potential targets for drug development, and predicting the effects of molecular interventions.

### How This Project Helps Scientists
This project would help scientists to automate the extraction and visualization of molecular interaction data from vast amounts of scientific literature, significantly reducing manual curation efforts. By integrating LLMs for natural language processing and utilizing platforms like NDEx and Cytoscape, the project aims to provide a powerful tool for exploring complex biological interactions, enhancing research productivity, and facilitating collaboration within the scientific community.

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
   
3. Developed the get interactions script: `python_scripts/get_interactions.py`. This script is responsible for reading in the prompt and running the extraction chain. The extraction chain was created using Langchain tools.

The extraction chain flows this way: prompt ----> extraction_model ----> Json_output_parser
4. Interacting with Indra Reach:
   
   a. Downloaded and installed Indra Reach API locally
   
   b. Utilized INDRA REACH to retrieve INDRA statements from PMCIDs: `python_scripts/get_indra_statements.py`
   
   c. Wrote code to get PMCIDs of papers that have PMIDs easily available: `python_scripts/get_pmcid.py`
   
5. Chunking_level Extraction: `python_scripts/chunking_level_extraction.py`.
   Implemented text chunking strategies to prepare large texts for processing through large language models (LLMs), facilitating the extraction of molecular interactions from segmented
   text. This was done using Langchain's textsplitter function.
   
7. Sentence_level Extraction: `python_scripts/sentence_level_extraction.py`
   
   a. Applied sentence-level extraction techniques to scientific documents using OpenAI API and INDRA REACH API to obtain precise interaction data. This was done by processing the statements gotten from indra to get only the sentences.
   
   b. This ensured that the same set of sentences were passed through the LLM first, then the indra reach api for processing sentence by sentence. Then the sentence, and the results from each of the API was noted.
   
8. Comparison and Evaluations:
   
   a. Modified the structure of the results gotten from both the indra reach and LLM to prepare it for evaluation as seen in the functions defined in the script,       
      `python_scripts/sentence_level_extraction.py`:
   ```
   combine_interaction
   create_combined_results
   combine_llm_and_indra_results
   ```
   b. Wrote code to compare the extracted interactions from both APIs and used F1_score as the evaluation metric. `python_scripts/evaluation_code.py`
   
9. Utilized Gilda grounding service to ground the genes, i.e convert to standard HGNC gene symbols that are involved in the interactions that were missed by the LLM and not grounded in order to get better evaluation results. The function is defined in this script: `python_scripts/grounding_genes.py`. Below are some examples that shows where the LLM succeeded in this and where it failed by comparing `results/pmc3898398/llm_combined_results.json` and `results/pmc3898398/grounded_llm_results.json`. 

   a. LLM successfully grounded:
      <p float="left">
        <img src="https://github.com/user-attachments/assets/b621ae56-5053-49ca-a9aa-ecb0b1f9b996" width="300" />
        <img src="https://github.com/user-attachments/assets/e1d31d8b-a42f-4232-907f-be1b565626eb" width="300" /> 
      </p>
   b. LLM unsuccessfully grounded:
      <p float="left">
        <img src="https://github.com/user-attachments/assets/c470204a-e5a4-474e-a429-779932940a48" width="300" />
        <img src="https://github.com/user-attachments/assets/5a970b08-9ba0-4e5a-8387-e788a92bcea9" width="300" /> 
      </p>
   c. Example where the grounding service failed:
      <p float="left">
        <img src="https://github.com/user-attachments/assets/e79912e1-1fa7-43fe-bfce-724f15b38ec1" width="300" />
        <img src="https://github.com/user-attachments/assets/88f9e5c8-2b0e-4b54-854e-9b3c332b27e6" width="300" /> 
      </p>


# Project Current State
1. Sentence_level extraction were performed on the paper with PMCID:pmc3898398 using the LLM and it was compared to the Indra Reach result and evaluated. The scores are shown below for the different trials: 

   a. For 50 sentences, comparison between `results/pmc3898398/grounded_llm_combined50.json` and `results/pmc3898398/indra_combined50_results.json`:
   ```
   Final Score:
   Precision (micro): 46.94%
      Recall (micro): 48.94%
         F1 (micro): 47.92%
   ```
   b. For comparison between `results/pmc3898398/llm_combined50_results.json` and `results/pmc3898398/indra_combined50_results.json`:
   ```
   Final Score:
   Precision (micro): 39.22%
      Recall (micro): 42.55%
         F1 (micro): 40.82%
   ```
   
   c. For all the sentences in the paper, comparison between `results/pmc3898398/grounded_llm_results.json` and `results/pmc3898398/indra_combined_results.json`:
   ```
   Final Score:
   Precision (micro): 25.41%
      Recall (micro): 31.08%
         F1 (micro): 27.96%
   ```
   d. For ungrounded llm results(for the whole paper), comparison between `results/pmc3898398/llm_combined_results.json` and `results/pmc3898398/indra_combined_results.json`:
   ```
   Final Score:
   Precision (micro): 18.52%
      Recall (micro): 23.65%
         F1 (micro): 20.77%
   ```
   
3. Processing time for the whole paper:

   a. With the Indra reach api: < 6 minutes
   
   b. With the OpenAI API: < 5 minutes

4. Best Performing prompt at the moment is: `papers/prompt_file_v3.txt`. The LLM is told to extract the interactions and resolve them to standard identifiers(grounding). The LLM is seen to do this perfectly for 

5. Some examples of the interactions gotten are shown below:
   - Example that show same interactions gotten for both indra and llm:
      <p float="left">
        <img src="https://github.com/user-attachments/assets/526b1d1d-f28f-4cbd-a7d7-d1ea65373d95" width="300" />
        <img src="https://github.com/user-attachments/assets/e51410e3-f803-425a-b7ca-32e7734a68a4" width="300" /> 
      </p>
      
   - In the example below, the LLM extracted several plausible biological interactions (such as "CLOCK RegulateAmount PER3", "PER1 Inhibition CLOCK", "CRY1 Inhibition BMAL1", etc.)    
     that, while possible within the context of circadian rhythm biology, were not directly mentioned in the provided sentence. These inferred interactions suggest that the LLM is 
     leveraging background biological knowledge to generate possible interactions that could be relevant in a broader biological context.
         <p float="left">
           <img src="https://github.com/user-attachments/assets/5fdb562e-ef71-4e28-9669-26f7ef4b5ba1" width="300" />
           <img src="https://github.com/user-attachments/assets/b1746303-be76-4ea8-aba9-5e2c830d183d" width="300" /> 
         </p>

   - In the example below, The LLM correctly identifies both interactions mentioned in the sentence: the regulation by p53 of miRNA-34 and the subsequent decrease in SIRT1 expression       by miRNA-34. INDRA's output does not capture the interactions described in the sentence. Instead, it suggests a self-inhibitory action by SIRT1 on itself, which is not relevant        to the given text.
        <p float="left">
           <img src="https://github.com/user-attachments/assets/7acfb7d4-1a2e-4388-89a5-27cf12f839f0" width="300" />
           <img src="https://github.com/user-attachments/assets/ea910d85-5604-49d1-b727-c11ce36bb9d6" width="300" /> 
        </p>

   - In the example below, The LLM incorrectly extracted that PARP2 inhibits SIRT1. The sentence indicates that inhibiting PARP2 leads to increased SIRT1 activity, not that PARP    
     directly inhibits SIRT1.
        <p float="left">
           <img src="https://github.com/user-attachments/assets/a5a1c04a-b1c6-4955-9961-03f4a54941d1" width="300" />
           <img src="https://github.com/user-attachments/assets/751234f0-e04a-4891-a597-0e5e826bb49" width="300" /> 
         </p>

   - In the example below, both the indra and the llm gave wrong interpretations of the sentence and therefore gave wrong outputs.
        <p float="left">
           <img src="https://github.com/user-attachments/assets/e119c5cb-3734-45a4-a147-058ae5af0ebc" width="300" />
           <img src="https://github.com/user-attachments/assets/82263567-40d5-43ae-ae5f-e10ca68734b6" width="300" /> 
        </p>

6. Converted extracted interactions to CX2 networks, uploaded them to NDEx for visaulisation using the script: `python_scripts/convert_to_cx2.py`. These networks can be viewed on         Favour James personal profile on NDEx here: https://www.ndexbio.org/viewer/networks/06a35259-6235-11ef-a7fd-005056ae23aa.
   The images below show the networks gotten from both the llm and indra for 50 sentences:

   <img width="500" alt="Screenshot 2024-08-24 at 19 56 55" src="https://github.com/user-attachments/assets/c77362ae-8941-4a4a-aed9-34a49a45c7b4">

  
# Future Tasks
  
- Develop a tool that enables users to upload scientific papers, extract molecular interactions, and automatically generate and upload networks to NDEx. This tool will facilitate seamless interaction with knowledge graphs and will serve as one of the pioneering "app" extensions for the new Cytoscape Web platform, enabling direct knowledge graph creation from scientific literature.
- Experiment with the model using various APIs, including Claude 3.5 Sonnet, to evaluate its performance and versatility.
- Apply prompt engineering techniques with Dspy to optimize prompt effectiveness and ensure the most efficient extraction of information.

# Challenges and Lessons Learned
## Lessons Learned
1. Advanced Prompt Engineering: Gained expertise in crafting detailed, efficient, and specific prompts for Large Language Models (LLMs) to optimize model interaction and enhance response accuracy.

2. API Integration and Usage: Developed proficiency in interfacing with the OpenAI API and INDRA Reach API, including making effective API calls and handling the responses for extracting biological interactions.

3. Schema Definition with Pydantic: Learned to utilize Pydantic functions to define robust model schemas, ensuring data validation and transformation into acceptable formats, particularly when integrating with LangChain for seamless data processing and model interaction.

4. Building Extraction Chains with LangChain: Mastered the use of LangChain to construct extraction chains, enabling complex multi-step reasoning processes and chained API calls. This included leveraging LangChain's capabilities to orchestrate API interactions for enriched data extraction workflows.

5. Modular Code Organization and GitHub Best Practices: Enhanced understanding of modularity and file organization within a GitHub repository to ensure maintainability, readability, and scalability of the project codebase.

6. Biological Interaction Types and Gene Grounding: Acquired knowledge on the various types of molecular interactions that occur between genes, as characterized by INDRA, and the importance of gene grounding. Learned techniques for ensuring accurate grounding of genes to improve data reliability and consistency.

7. Enhanced Understanding of Gene Grounding: Explored the concept of gene grounding in detail, focusing on techniques to ensure correct mapping and standardization of gene names across different databases and ontologies, crucial for accurate biological data interpretation.

## Technologies Learnt
During my GSoC project, I explored several new technologies and the most interesting ones were:
1. LangChain: A framework for building applications powered by language models. It was fascinating to see how LangChain enables chaining multiple LLM interactions, creating more sophisticated natural language processing workflows.

2. INDRA (Integrated Network and Dynamical Reasoning Assembler): A system for extracting, standardizing, and modeling scientific knowledge. It was intriguing to see how INDRA automates the conversion of unstructured biological data into structured formats for easier analysis using REACH.

One of the most captivating concepts was **knowledge graphs**, which represent complex biological interactions from various sources. Building these graphs from scientific texts was enlightening, showing how interconnected biological data can be visualized and analyzed for new insights. Additionally, prompt engineering for LLMs was a critical skill learned, highlighting how carefully crafted prompts can improve model outputs and drive better results in NLP tasks.
  
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
- https://ndex2.readthedocs.io/en/latest/index.html

