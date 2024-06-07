import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from model import extraction_model
warnings.filterwarnings("ignore")


# Write a prompt for extracting molecular interactions
template = """
Extract all molecular interactions from the provided scientific text. The subject should be the first entity 
interacting with the second entity which is the object. Then the activity between the two entities should be the 
interaction type. The results should look like the examples below:
      "type": "Activation",
      "subj": "NS1",
      "obj": "HPA-1",
          "text": "Nonstructural protein 1 (NS1) of dengue virus (DENV) can stimulate endothelial cells to secrete 
          endothelial hyperpermeability factor, macrophage migration inhibitory factor (MIF), and the glycocalyx 
          degradation factor heparanase 1 (HPA-1)."
    "type": "Inhibition",
      "subj": "NS1",
      "obj": "macrophage migration inhibitory factor (MIF)"
          "text": "Nonstructural protein 1 (NS1) of dengue virus (DENV) can stimulate endothelial cells to secrete 
          endothelial hyperpermeability factor, macrophage migration inhibitory factor (MIF), and the glycocalyx 
          degradation factor heparanase 1 (HPA-1)."
In the example above, notice that the subj is the first gene and the second gene is the obj and the subj is the one
interacting with the obj, then the text is the the sentence from which the interaction was taken from. Please 
do not paraphrase the sentences, it should be exactly the same sentence that is passed to the chain.
"""

# Define the extraction chain
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="interactions")
