from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils import get_columns_from_text, get_properties_from_details
from strings import DATABASE_BASIC_PROPERTIES

llm = OpenAI(temperature=0.7)

template = """{statement}

For the above statement, what database columns should I use. (enumerate with numbers)
"""
prompt_template = PromptTemplate(input_variables=["statement"], template=template)
properties_chain = LLMChain(llm=llm, prompt=prompt_template)


names = [x[0] for x in get_properties_from_details(DATABASE_BASIC_PROPERTIES)]
types = ", ".join(names)
# This is an LLMChain to write a review of a play given a synopsis.
template = """
{result}

What are the type for the following properties from the given available types: {types}

1. {Title} : Title
"""
prompt_template = PromptTemplate(
    input_variables=["types", "result", "Title"], template=template
)
property_type_chain = LLMChain(llm=llm, prompt=prompt_template)

# This is the overall chain where we run these two chains in sequence.
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(chains=[properties_chain], verbose=True)

database_properties_string = overall_chain.run(
    "I need to create a 2023 goal tracker table. I need to have a status column please"
)
database_properties_string = """1. Goal 
2. Start Date 
3. End Date 
4. Status 
5. Notes"""
database_properties = get_columns_from_text(database_properties_string)
title = database_properties[0].strip()
print(title)
# database_types_string = property_type_chain(
#     {"types": types, "Title": title, "result": database_properties_string}
# )
# print(database_types_string)
