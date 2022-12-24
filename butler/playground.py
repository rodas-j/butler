from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import get_columns_from_text

llm = OpenAI(temperature=0.7)

template = """{statement}

For the above statement, what database columns should I use. (enumerate with numbers)
"""
prompt_template = PromptTemplate(input_variables=["statement"], template=template)
properties_chain = LLMChain(llm=llm, prompt=prompt_template)


# This is an LLMChain to write a review of a play given a synopsis.
# llm = OpenAI(temperature=.7)
# template = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.

# Play Synopsis:
# {synopsis}
# Review from a New York Times play critic of the above play:"""
# prompt_template = PromptTemplate(input_variables=["synopsis"], template=template)
# review_chain = LLMChain(llm=llm, prompt=prompt_template)

# # This is the overall chain where we run these two chains in sequence.
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(chains=[properties_chain], verbose=True)

review = overall_chain.run(
    "I need to create a 2023 goal tracker table. I need to have a status column please"
)
