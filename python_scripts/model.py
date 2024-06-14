import os
import warnings
import time
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain_core.utils.function_calling import convert_pydantic_to_openai_function
from langchain_openai import ChatOpenAI
warnings.filterwarnings("ignore")

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


# Define a function that adds a delay to a Completion API call
def delayed_completion(delay_in_seconds: float = 1, **kwargs):
    """Delay a completion by a specified amount of time.""" 
    time.sleep(delay_in_seconds)
    return ChatOpenAI(**kwargs)


rate_limit_per_minute = 3
delay = 60.0 / rate_limit_per_minute


class Interaction(BaseModel):
    """Information about molecular interactions mentioned."""
    subject: str = Field(..., description="Entity that is the first involved in the interaction")
    object: str = Field(..., description="Entity that is the second involved in the interaction")
    interaction_type: str = Field(..., description="This shows the activity or type of interaction going on between the\
        subject and the object")
    Text: str = Field(..., description="The exact sentence from which the interacting subject and object is taken from")
    direct: str = Field(..., description="This captures where there is a physical interaction between the subject and \
        object. If there is a physical relationship, then response is True. Otherwise, response is False")
    hypothesis: str = Field(..., description="This captures if an interaction is known (from previous or the current \
        study) versus the authors think it might exist but have not verified it. If suggested by authors, then true. \
            Otherwise, response is false")


class Molecular_Interactions(BaseModel):
    """Information to extract."""
    interactions: List[Interaction]


paper_extraction_function = [
    convert_pydantic_to_openai_function(Molecular_Interactions)
]

# Define model for extraction
model = delayed_completion(delay_in_seconds=delay, model="gpt-3.5-turbo",
                           temperature=0, openai_api_key=OPENAI_API_KEY)


extraction_model = model.bind(
    functions=paper_extraction_function,
    function_call={"name": "Molecular_Interactions"}
)
