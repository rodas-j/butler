from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from butler.utils import get_columns_from_text, get_properties_from_details
from butler.strings import DATABASE_BASIC_PROPERTIES
from langchain.chains import SimpleSequentialChain

types = "Title, Text, Number, Select, Multi-select, Status, Date, Person, Files & media, Checkbox, URL, Email, Phone"


propertyNotation = {
    "title": "title",
    "text": "rich_text",
    "number": "number",
    "select": "select",
    "multi-select": "multi_select",
    "status": "status",
    "date": "date",
    "person": "people",
    "files & media": "files",
    "checkbox": "checkbox",
    "url": "url",
    "email": "email",
    "phone": "phone_number",
}

# add values as keys and values as values
propertyNotation.update({v: v for _, v in propertyNotation.items()})


def handleOptions(js_objects, filtered_tuples, database_properties_string, llm):

    template = """{result}

    give no more than five examples for {properties} (comma separated)

    {prop}:"""

    prompt_template = PromptTemplate(
        input_variables=["result", "properties", "prop"], template=template
    )

    property_type_chain = LLMChain(llm=llm, prompt=prompt_template)

    select_multi_select_ = list(map(lambda x: x[0], filtered_tuples))

    example_options_string = property_type_chain.run(
        {
            "prop": select_multi_select_[0],
            "properties": ", ".join(select_multi_select_),
            "result": database_properties_string,
        }
    )
    example_options_list = example_options_string.split("\n")
    options_dict = {
        select_multi_select_[0]: example_options_list[0].strip().split(","),
    }
    for i in range(1, len(example_options_list)):
        options_dict[select_multi_select_[i]] = (
            example_options_list[i].split(": ")[1].split(",")
        )
    import random

    for obj in js_objects:
        if obj["name"] in options_dict:
            options_list = list(
                map(
                    lambda x: {
                        "name": x.strip(),
                        "color": random.choice(
                            [
                                "default",
                                "gray",
                                "brown",
                                "orange",
                                "yellow",
                                "green",
                                "blue",
                                "purple",
                                "pink",
                                "red",
                            ]
                        ),
                    },
                    options_dict[obj["name"]],
                )
            )
            obj["options"] = options_list


def queryOpenAI(message: str):
    llm = OpenAI(
        temperature=0.7,
        openai_api_key="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",
    )

    template = """{statement}

    For the above statement, what database columns should I use. (enumerate with numbers)
    """
    prompt_template = PromptTemplate(input_variables=["statement"], template=template)
    properties_chain = LLMChain(llm=llm, prompt=prompt_template)

    overall_chain = SimpleSequentialChain(chains=[properties_chain], verbose=True)

    database_properties_string = overall_chain.run(message)
    database_properties = get_columns_from_text(database_properties_string)

    template = """
    {result}

    What are the type for the following properties from the given available types: {types}

    1. {Title}: Title
    """

    prompt_template = PromptTemplate(
        input_variables=["types", "result", "Title"], template=template
    )

    property_type_chain = LLMChain(llm=llm, prompt=prompt_template)

    first_title = database_properties[0]

    assert type(first_title) == str
    # type: ignore
    database_types_string = property_type_chain.run(
        {"Title": first_title, "types": types, "result": database_properties_string}
    )

    result_types = list(
        map(
            lambda x: x.split(":")[1].strip(),
            get_columns_from_text(database_types_string),
        )
    )
    result_types.insert(0, "Title")
    result_types = list(
        map(
            lambda x: propertyNotation.get(x.lower().split(",")[0], "multi_select"),
            result_types,
        )
    )

    assert len(database_properties) == len(result_types)

    tuples = zip(database_properties, result_types)

    tuples = list(tuples)

    database_description = handleDetails(message, llm)

    information_dictionary = dict(get_properties_from_details(database_description))

    # assert information_dictionary.keys() == {
    #     "Title",
    #     "Description",
    #     "Emoji",
    # }, information_dictionary

    filtered_tuples = list(
        filter(
            lambda x: propertyNotation[x[1].lower()] in ["select", "multi_select"],
            tuples,
        )
    )

    js_objects = []
    for tup in tuples:
        js_objects.append({"name": tup[0], "type": tup[1]})

    handleOptions(js_objects, filtered_tuples, database_properties_string, llm)

    js_response = {
        "title": information_dictionary.get("Title", "Untitled"),
        "description": information_dictionary.get("Description", "No description"),
        "icon": {
            "type": "emoji",
            "emoji": information_dictionary.get("Emoji", "default"),
        },
        "properties": js_objects,
    }
    print(js_response)

    return js_response


def handleDetails(message, llm):
    template = """{statement}
    What is the best information for the following
    Title:
    Description:
    Emoji:"""

    prompt_template = PromptTemplate(input_variables=["statement"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)

    overall_chain = SimpleSequentialChain(chains=[chain], verbose=True)

    database_description = overall_chain.run(message)
    return database_description


if __name__ == "__main__":
    print(
        queryOpenAI(
            "I need to create a 2023 goal tracker table. I need to have a status column please"
        )
    )
