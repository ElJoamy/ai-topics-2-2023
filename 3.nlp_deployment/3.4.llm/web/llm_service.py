from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import get_settings
from prompts import PROMPT_TEMPLATE, ProjectParams
from parsers import get_project_parser, ProjectIdeas

_SETTINGS = get_settings()


class TemplateLLM:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model=_SETTINGS.model, openai_api_key=_SETTINGS.openai_key
        )
        self.parser = get_project_parser()
        self.prompt_template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["major", "n_examples", "language"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def generate(self, params: ProjectParams) -> ProjectIdeas:
        _input = self.prompt_template.format(**params.model_dump())
        output = self.llm.predict(_input)
        return self.parser.parse(output)
    
    