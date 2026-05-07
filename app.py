import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import PydanticOutputParser


class TaskPlanner(BaseModel):
    goal: str
    duration: str
    steps: List[str]

model = ChatGroq(model="llama-3.3-70b-versatile")
parser = PydanticOutputParser(pydantic_object=TaskPlanner)

template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a professional task planner who breaks goals
        into step-by-step plans in terms of days, weeks, or months.
        You should not answer topics other than planning tasks.
        If asked, reply you are not trained on that topic.
        {format_instructions}"""),
        ("human", "{prompt}")
    ]
)


st.title("🎯 AI Task Planner")
st.write("Enter your goal and get a structured step-by-step plan!")

user_input = st.text_input("Enter your goal")

if st.button("Generate Plan"):
    if user_input.strip() == "":
        st.warning("Please enter a goal!")
    else:
        with st.spinner("Generating your plan..."):
            
            # Your manual approach (no chain)
            final_prompt = template.invoke(
                {
                    "prompt": user_input,
                    "format_instructions": parser.get_format_instructions()
                }
            )

            response = model.invoke(final_prompt)
            parser_output = parser.parse(response.content)


        st.success("Plan Generated!")

        st.subheader("🎯 Goal")
        st.write(parser_output.goal)

        st.subheader("⏳ Duration")
        st.write(parser_output.duration)

        st.subheader("📋 Steps")
        for i, step in enumerate(parser_output.steps, 1):
            st.write(f"**Step {i}:** {step}")