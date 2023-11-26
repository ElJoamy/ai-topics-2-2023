from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class ProjectTemplate(BaseModel):
    title: str
    problem_definition: str
    justification: str
    main_goal: str


class ProjectIdeas(BaseModel):
    major: str
    ideas: list[ProjectTemplate]


def get_project_parser():
    return PydanticOutputParser(pydantic_object=ProjectIdeas)