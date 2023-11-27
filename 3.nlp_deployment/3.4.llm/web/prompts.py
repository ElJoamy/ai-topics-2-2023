from enum import Enum
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate


PROMPT_TEMPLATE = """You are an {major} senior student looking for a final project for graduation.
    In order to classify for your dissertation you need to present a project proposal with the following
    parts: 
    - Title
    - Hypothesis
    - Problem to solve
    - Justification
    - Main objective
    Generate {n_examples} examples for final projects with the given format in {language} language
    using the {format_instructions}.
    """


class Major(str, Enum):
    civil_engineering = "civil engineering"
    electrical_computer_engineering = "electrical and computer engineering"
    computer_science = "computer science"
    industrial_engineering = "industrial engineering"
    chemical_engineering = "chemical engineering"


class Language(str, Enum):
    spanish = "spanish"
    english = "english"


class ProjectParams(BaseModel):
    major: Major
    language: Language
    n_examples: int = Field(default=2, lt=4)
