import os
import warnings
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.utils.function_calling import convert_pydantic_to_openai_function
from langchain_openai import ChatOpenAI
warnings.filterwarnings("ignore")


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
model = ChatOpenAI(model = "gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

# Define Pydantic models for the data we want to extract
class Interaction(BaseModel):
    """Information about molecular interactions mentioned."""
    entities_involved: List[str]
    interaction_type: str
    interaction_details: Optional[str]

class Molecular_Interactions(BaseModel):
    """Information to extract."""
    interactions: List[Interaction]
    
# Convert the pydantic classes to openai model   
paper_extraction_function = [
    convert_pydantic_to_openai_function(Molecular_Interactions)
]
extraction_model = model.bind(
    functions=paper_extraction_function,
    function_call={"name":"Molecular_Interactions"}
)

