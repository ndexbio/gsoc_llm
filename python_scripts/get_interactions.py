import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from model import extraction_model
warnings.filterwarnings("ignore")

#explain what subject, object, interaction type, hypothesis, direct
# Write a prompt for extracting molecular interactions
template = """
Extract all molecular interactions from the provided scientific text. The subject should be the first entity 
interacting with the second entity which is the object. Then the activity between the two entities should be the 
interaction type. For the interaction types, you should make use of the interaction types present in the 
indra database, that is, you should use the same names used to describe interaction types in Indra database 
interactions. The results should look like the examples below:
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
    "type": "Activation",
      "subj": "NS1",
      "obj": "HPA-1",
          "text": "According to a previous study, NS1 can induce endothelial cells to secrete HPA-1 to disrupt the 
          endothelial glycocalyx, and this disruption is characterized by CD138 shedding [18].",
          "epistemics":
            "hypothesis": true,
            "direct": false       
      "type": "Activation",
      "subj": "NS1",
      "obj": "HPA-1",
          "text": "To further investigate the underlying mechanism of NS1-induced HPA-1 secretion, human umbilical 
          vein endothelial cells (HUVECs) were stimulated with NS1 for various durations.",
          "epistemics": 
            "direct": false,
            "hypothesis": false
In the example above, notice that the subj is the first gene and the second gene is the obj and the subj is the one
interacting with the obj, then the text is the the sentence from which the interaction was taken from. Please 
do not paraphrase the sentences, it should be exactly the same sentence that is passed to the chain. 
Also extract responses for the direct and hypothesis variable. Direct is true if there is a direct \
relationship/interaction between the subject and object. Then hypothesis is true if the interaction is suggested \
by the authors.
"""
#only use the indra database interaction types
#hypothesis: hypothesis is true if the interaction is only suggested.
#direct: direct means there is actual physical interaction between the subject and the objects. if there is an actual 
# interaction/relationship between the subject and object, then true. if not, false.

# Define the extraction chain
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="interactions")
