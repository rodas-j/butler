# make a Database class with the builder pattern

from langchain import LLMChain, PromptTemplate
from langchain.chains import SequentialChain, TransformChain
from butler.config import llm, propertyNotation
from typing import List
from butler.utils import get_columns_from_text, get_properties_from_details

types = "Title, Text, Number, Select, Multi-select, Status, Date, Person, Files & media, Checkbox, URL, Email, Phone"


class DatabaseChain:
    def __init__(self, prompt):
        self.prompt = prompt
        self.database_properties: List
        self.tuples: List[str]
        self.chains: List = []
        self.input_variables: List[str] = ["statement", "types"]
        self.output_variables: List[str] = []
        self.output: dict = {}
        self.build()

    def build(self):
        self.add_columns()
        self.add_property_types()
        self.add_options()
        self.add_content()
        self.add_details()

        self.overall_chain = SequentialChain(
            chains=self.chains,  # type: ignore
            input_variables=self.input_variables,
            output_variables=self.output_variables,
            verbose=True,
        )

        self.output = self.overall_chain(
            {
                "statement": self.prompt,
                "types": types,
            }
        )
        self.post_process()

    def add_columns(self):
        template = """{statement}

        For the above statement, what database columns should I use. (enumerate with numbers)
        """
        prompt_template = PromptTemplate(
            input_variables=["statement"], template=template
        )
        self.columns_chain = LLMChain(
            llm=llm, output_key="result", prompt=prompt_template
        )
        self.chains.append(self.columns_chain)
        self.output_variables.append("result")

    def _transform_func(self, inputs: dict) -> dict:
        columns = get_columns_from_text(inputs["result"])
        first_column = columns[0]
        return {"Title": first_column}

    def _transform_property_type(self, inputs: dict) -> dict:
        result_types = list(
            map(
                lambda x: x.split(":")[1].strip(),
                get_columns_from_text(inputs["property_types"]),
            )
        )
        result_types.insert(0, "Title")
        result_types = list(
            map(
                lambda x: propertyNotation.get(x.lower().split(",")[0], "multi_select"),
                result_types,
            )
        )

        self.database_properties = get_columns_from_text(inputs["result"])

        assert len(self.database_properties) == len(result_types)

        tuples = zip(self.database_properties, result_types)

        tuples = list(tuples)

        self.filtered_tuples = list(
            filter(
                lambda x: propertyNotation[x[1].lower()] in ["select", "multi_select"],
                tuples,
            )
        )

        self.select_multi_select_ = list(map(lambda x: x[0], self.filtered_tuples))

        self.js_objects = []
        for tup in tuples:
            self.js_objects.append({"name": tup[0], "type": tup[1]})
        return {
            "prop": self.select_multi_select_[0],
            "properties": ", ".join(self.select_multi_select_),
        }

    def add_property_types(self):

        self.columns_transform_chain = TransformChain(
            input_variables=["result"],
            output_variables=["Title"],
            transform=self._transform_func,
        )

        self.chains.append(self.columns_transform_chain)

        template = """
        {result}

        What are the type for the following properties from the given available types: {types}

        1. {Title}: Title
        """

        prompt_template = PromptTemplate(
            input_variables=["types", "result", "Title"], template=template
        )

        self.property_type_chain = LLMChain(
            llm=llm, prompt=prompt_template, output_key="property_types"
        )
        self.chains.append(self.property_type_chain)
        self.output_variables.append("property_types")

        self.property_type_transform_chain = TransformChain(
            input_variables=["property_types"],
            output_variables=["prop", "properties"],
            transform=self._transform_property_type,
        )
        self.chains.append(self.property_type_transform_chain)

    def _process_details(self, details):
        return dict(get_properties_from_details(details))

    def post_process(self):
        description_information = self._process_details(self.output["details"])
        self.output["table_metadata"] = description_information
        example_options_string = self.output.get("options", "")
        example_options_list = example_options_string.split("\n")
        options_dict = {
            self.select_multi_select_[0]: example_options_list[0].strip().split(","),
        }
        for i in range(1, len(example_options_list)):
            options_dict[self.select_multi_select_[i]] = (
                example_options_list[i].split(": ")[1].split(",")
            )
        import random

        for obj in self.js_objects:
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
        self.output.update({"js_objects": self.js_objects})

    def add_options(self):

        template = """{result}

        give no more than five examples for {properties} (comma separated)

        {prop}:"""

        prompt_template = PromptTemplate(
            input_variables=["result", "properties", "prop"], template=template
        )

        self.options_chain = LLMChain(
            llm=llm, prompt=prompt_template, output_key="options"
        )

        self.chains.append(self.options_chain)
        self.output_variables.append("options")

    def add_content(self):
        pass

    def add_details(self):
        template = """{statement}
        
        The following are the columns in the database
        {result}
        
        What is the best information for the following
        Title:
        Description:
        Emoji:"""

        prompt_template = PromptTemplate(
            input_variables=["statement", "result"], template=template
        )
        details_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="details")

        self.chains.append(details_chain)
        self.output_variables.append("details")

    def compile(self):
        pass


if __name__ == "__main__":
    output = DatabaseChain(prompt="I want to make a database to track my books")
