# GSoC_LLM Project
This project proposes the development of a Python web application that utilizes Large Language Models (LLMs) for extracting, transforming, and visualizing molecular interaction networks from scientific literature. Leveraging LLMs' advanced natural language processing capabilities, the application will interpret complex academic texts to construct interaction graphs.

## Prerequisites
Python (version 3.6 or higher)

pip (Python package installer)

## Setting up
1. Clone this repo to your local system
2. (Optional) Create and Activate a Virtual Environment
To avoid installing dependencies globally and keep your system clean, you can create and activate a virtual environment for this project.
3. Install dependencies using: pip install -r requirements.txt
   
## Extraction Task
To perform the task of extracting interactions from the scientific paper with PMCID:PMC389839, follow the steps listed below:

1. Run this script: python_scripts/model.py
2. Next, run this script: python_scripts/get_interactions.py
3. Then, run this script: python_scripts/sentence_level_comparison.py

