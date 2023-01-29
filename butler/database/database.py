# make a Database class with the builder pattern

from langchain import LLMChain, PromptTemplate
from langchain.chains import SequentialChain, TransformChain
from butler.config import llm, propertyNotation, COLORS
from typing import Any, Dict, List, Tuple
from butler.utils import get_columns_from_text, get_properties_from_details
from logger import logger


types = "Title, Text, Number, Select, Multi-select, Status, Date, Person, Files & media, Checkbox, URL, Email, Phone"


class DatabaseChain:
    def __init__(self, prompt):
        self.prompt = prompt
        self.select_multi_select_: List[str] = []
        self.columns: List[str] = []
        self.is_select_multi_select_excluded = False
        self.database_properties: List
        self.tuples: List[str]
        self.chains: List = []
        self.js_objects = []
        self.input_variables: List[str] = ["statement", "types"]
        self.output_variables: List[str] = []
        self.output: dict = {}
        self.build()

    def build(self):
        self.add_columns()
        self.add_property_types()
        if not self.is_select_multi_select_excluded:
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
        logger.info("Built database chain")

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
        logger.info("Added columns chain")

    def remove_parenthesis(self, s: str):
        import re

        return re.sub(r"\(.*\)", "", s).strip()

    def _transform_func(self, inputs: dict) -> dict:
        self.columns: List[str] = get_columns_from_text(inputs["result"])

        first_column = self.columns[0]
        self.columns = list(map(self.remove_parenthesis, self.columns))
        return {"Title": first_column, "columns": ",".join(self.columns)}

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
        self.database_properties = list(
            map(self.remove_parenthesis, self.database_properties)
        )

        assert len(self.database_properties) == len(result_types)

        tuples = zip(self.database_properties, result_types)

        tuples_list: List[Tuple[Any, Any]] = list(tuples)

        self.filtered_tuples = list(
            filter(
                lambda x: propertyNotation[x[1].lower()] in ["select", "multi_select"],
                tuples_list,
            )
        )

        self.select_multi_select_ = list(map(lambda x: x[0], self.filtered_tuples))

        for tup in tuples_list:
            self.js_objects.append({"name": tup[0], "type": tup[1]})
        logger.info("Added property types chain")

        if len(self.select_multi_select_) == 0:
            self.is_select_multi_select_excluded = True
            logger.info("No select or multi-select properties")
            return {"prop": "", "properties": ""}

        return {
            "prop": self.select_multi_select_[0],
            "properties": ", ".join(self.select_multi_select_),
        }

    def add_property_types(self):

        self.columns_transform_chain = TransformChain(
            input_variables=["result"],
            output_variables=["Title", "columns"],
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
        if not self.is_select_multi_select_excluded:
            self.chains.append(self.property_type_transform_chain)

    def _process_details(self, details):
        return dict(get_properties_from_details(details))

    def _process_content(self, content: str):
        from io import StringIO
        import pandas as pd

        overall_csv = ",".join(self.columns).strip() + "\n" + content.strip()
        log_csv = "\n" + str(overall_csv) + "\n"
        logger.info(log_csv)

        table = pd.read_csv(StringIO(overall_csv))

        # change NaN to empty string
        table = table.fillna("")
        table = table.astype(str)

        # strip whitespace
        table = table.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        date_columns = list(filter(lambda x: "date" in x.lower(), table.columns))
        for column in date_columns:
            try:
                table[column] = pd.to_datetime(table[column]).dt.strftime("%Y-%m-%d")
            except Exception as e:
                logger.error(f"Error converting {column} to date: {e}")
                table[column] = "2020-09-01"
        return table.to_dict("records")

    def process_options(self):
        example_options_string: str = self.output.get("options", "")
        example_options_list: List[str] = example_options_string.split("\n")
        options_dict: Dict[str, List[str]] = {}
        assert len(example_options_list) == len(
            self.select_multi_select_
        ), f"Contents of options list: {example_options_list} and select_multi_select_: {self.select_multi_select_}"
        for i in range(
            1, len(list(zip(example_options_list, self.select_multi_select_)))
        ):

            options_dict[self.select_multi_select_[i]] = (
                example_options_list[i].split(": ")[1].strip().split(",")
            )
        import random

        for obj in self.js_objects:
            if obj["name"] in options_dict:
                options_list = list(
                    map(
                        lambda x: {
                            "name": x.strip(),
                            "color": random.choice(COLORS),
                        },
                        options_dict[obj["name"]],
                    )
                )
                obj["options"] = options_list

    def post_process(self):
        description_information = self._process_details(self.output["details"])
        self.output["table_metadata"] = description_information
        self.output["prompt"] = self.prompt

        try:
            self.output["content_json"] = self._process_content(self.output["content"])
        except Exception as e:
            logger.error(e)
            logger.error("self.output does not have content")
            self.output["content_json"] = []
        if not self.is_select_multi_select_excluded:
            self.process_options()
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
        logger.info("Added options")

    def add_content(self):
        template = """
        1. {Title}: Title
        {property_types}
        
        Create 3 to 5 examples for the table with the columns listed above (The columns must match the ones listed above). Make it in csv format.
        
{columns}
"""  # DONOT CHANGE THIS LINE

        prompt_template = PromptTemplate(
            input_variables=["Title", "property_types", "columns"], template=template
        )
        content_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="content")

        self.chains.append(content_chain)
        self.output_variables.append("content")
        logger.info("Added content")

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
        logger.info("Added details")


if __name__ == "__main__":
    output = DatabaseChain(prompt="I want to make a database to track my books")
