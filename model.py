from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import  BaseModel
from typing import List
from langchain_core.output_parsers import PydanticOutputParser

class TaskPlanner(BaseModel):
    goal : str
    duration : str
    steps : List[str]

model = ChatGroq(model="llama-3.3-70b-versatile")

template = ChatPromptTemplate.from_messages(
    [
        ("system","You are a professional task planner who plan the given goal and breaks the goal into step by step guide in terms  of days, weeks or months as per the user interests.You should not answer to the topics other than planning tasks, if asked reply you are not trained on the specific topic given by the user and say I am an agent built to plan the goals as per needs. {format_instructions}"),
        ("human","{prompt}")
    ]
)

parser = PydanticOutputParser(pydantic_object=TaskPlanner)

prompt = input("Enter you are task: ")

final_prompt = template.invoke(
    {"prompt":prompt,
     "format_instructions":parser.get_format_instructions()}
)

response = model.invoke(final_prompt)
parser_output = parser.parse(response.content)
print(parser_output)