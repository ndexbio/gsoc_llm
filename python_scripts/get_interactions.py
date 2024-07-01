import warnings
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from model import extraction_model
warnings.filterwarnings("ignore")

#explain what subject, object, interaction type, hypothesis, direct
# Write a prompt for extracting molecular interactions
template = """
Extract all molecular interactions from the provided scientific text. The subject should be the first molecular entity 
interacting with the second molecular entity which is the object. Then the activity between the two entities should be 
the interaction type. For the interaction types, you should make use of the interaction types present in the 
indra database, that is, you should use the same names used to describe interaction types in Indra database 
interactions. The results should look like the examples below:
"subject": "adrenocorticotropic hormone",
        "object": "adenylate cyclase",
        "interaction_type": "Activation",
        "text": "The adenylate cyclase of this corticosteroid-producing, transplanted, adrenal cancer of the rat was 
        stimulated not only by adrenocorticotropic hormone and fluoride, but also by the f8-adrenergic agonist, 
        isoproterenol.",
        "direct": true,
        "hypothesis": false
"subject": "isoproterenol",
        "object": "adenylate cyclase",
        "interaction_type": "Inhibition",
        "text": "The adenylate cyclase of normal adrenal tissue was unresponsive to isoproterenol.",
        "direct": true,
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
