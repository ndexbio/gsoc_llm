# GSoC_LLM Project
This project proposes the development of a Python web application that utilizes Large Language Models (LLMs) for extracting, transforming, and visualizing molecular interaction networks from scientific literature. This project is leveraging LLMs' advanced natural language processing capabilities, the application will interpret complex academic texts to construct interaction graphs. These results would be uploaded to the Network Data Exchange (NDEx) platform, enabling researchers to manage and visualize biological data more effectively.

## Prerequisites
Python (version 3.6 or higher)

## Installation
1. Create and Activate a Virtual Environment: It is good practice to do this to avoid installing dependencies globally and keep your system clean:
   
   Using Conda: `conda create -n myenv python==3.11` and activate it with `conda activate myenv`
   
   Using venv: `python3.8 -m venv myenv`, activate with `python3.8 -m venv myenv` on MacOS/Linux and `myenv\Scripts\activate` on Windows
   
2. Install dependencies using: `pip install -r requirements.txt`
   
## Extraction Task
To perform the task of extracting interactions from the scientific paper, follow the steps listed below:

1. Run this script: python_scripts/model.py
2. Next, run this script: python_scripts/get_interactions.py
3. Then, run this script: python_scripts/sentence_level_comparison.py

