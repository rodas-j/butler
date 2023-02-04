import json
from typing import List
from pytest import MonkeyPatch
import pandas as pd

from butler.database.database import DatabaseChain, LLMChain, SequentialChain
from unittest.mock import MagicMock, Mock
import unittest.mock as mock
import pytest


def mock_overall(*args, **kwargs):
    with open("tests/test_data/database/openaimock/mock.json") as f:
        mock_list: List[dict] = json.load(f)
        return mock_list[1]


@pytest.fixture
def openai_mock_fixture():
    with mock.patch("butler.database.database.SequentialChain") as mock_SequentialChain:
        yield mock_SequentialChain


# patch langchain.chains.SequentialChain with mock_overall using magic mock
@pytest.fixture
def mock_SequentialChain(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "butler.database.database.SequentialChain",
        MagicMock(return_value=mock_overall),
    )
    monkeypatch.setattr(
        "butler.database.database.DatabaseChain.build", lambda *args, **kwargs: "test"
    )


def remove_keys(d: dict, keys: List[str]) -> dict:
    for key in keys:
        d.pop(key, None)
    return d


class TestDatabaseChain:
    def test_mock_overall(self):
        overall = mock_overall()
        assert overall["content"] != None

    def test_database_chain(self, mock_SequentialChain):
        DatabaseChain("test")

    def test_add_columns(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            "butler.database.database.DatabaseChain.build",
            lambda *args, **kwargs: "test",
        )
        monkeypatch.setattr(
            "butler.database.database.LLMChain", lambda *args, **kwargs: "test"
        )

        chain = DatabaseChain(prompt="test")
        chain.add_columns()

        mack = MagicMock()
        mack.return_value = "test"

        assert chain.chains == ["test"]

        assert chain.output_variables == ["result"]

    def test_post_process(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            "butler.database.database.DatabaseChain.build",
            lambda *args, **kwargs: "test",
        )
        monkeypatch.setattr(
            "butler.database.database.LLMChain", lambda *args, **kwargs: "test"
        )

        chain = DatabaseChain(prompt="test")
        chain.output = {
            "content": '"Crispy Fried Chicken,""2 pounds boneless chicken thighs or breasts, cut into small pieces, 2 tablespoons salt, 2 tablespoons black pepper, 2 tablespoons garlic powder, 2 tablespoons onion powder, 2 tablespoons paprika, 1 cup all-purpose flour, 1/2 cup cornstarch, 2 cups vegetable oil,""In a large bowl, combine the chicken pieces, salt, pepper, garlic powder, onion powder and paprika. Toss until all the chicken pieces are evenly coated. In a separate bowl, mix together the flour and cornstarch. Dip the chicken pieces into the flour mixture and coat them evenly. Heat the oil in a large skillet on medium-high heat. Add the chicken pieces to the skillet and cook for about 10 minutes, or until golden brown and crispy. Remove the chicken from the skillet and serve,"4,15 minutes,25 minutes,Medium,Per Serving: Calories: 556; Fat: 35.4g; Carbohydrates: 24.6g; Protein: 30.2g,Southern,Main Dish',
            "details": "\n\nTitle: Delicious Recipes for Every Occasion\nDescription: This recipe book is filled with flavorful and easy-to-follow recipes for breakfast, lunch, dinner, and desserts. Whether you're looking for a quick dinner or a gourmet dessert, you'll find something to satisfy everyone's appetite. \nEmoji: 🍽️",
            "options": " Easy, Medium, Hard, Very Hard, Extremely Hard\n\n        Cuisine or Type of Dish: Italian, Mexican, Chinese, Japanese, Thai\n\n        Category or Course: Main Dish, Appetizer, Dessert, Soup, Salad",
            "property_types": "2. Ingredients: Text\n        3. Instructions: Text\n        4. Serving Size: Number\n        5. Prep Time: Date\n        6. Cook Time: Date\n        7. Difficulty Level: Select, Multi-select\n        8. Nutrition Information: Text\n        9. Cuisine or Type of Dish: Select, Multi-select\n        10. Category or Course: Select, Multi-select",
            "result": "\n1. Recipe Name\n2. Ingredients\n3. Instructions\n4. Serving Size\n5. Prep Time\n6. Cook Time \n7. Difficulty Level\n8. Nutrition Information\n9. Cuisine or Type of Dish\n10. Category or Course",
            "statement": "I want to make a recipe book",
            "types": "Title, Text, Number, Select, Multi-select, Status, Date, Person, Files & media, Checkbox, URL, Email, Phone",
        }
        # chain.is_select_multi_select_excluded = True
        chain.post_process()

    def test_process_content(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            "butler.database.database.DatabaseChain.build",
            lambda *args, **kwargs: "test",
        )

        chain = DatabaseChain(prompt="test")
        content = '"Crispy Fried Chicken,""2 pounds boneless chicken thighs or breasts, cut into small pieces, 2 tablespoons salt, 2 tablespoons black pepper, 2 tablespoons garlic powder, 2 tablespoons onion powder, 2 tablespoons paprika, 1 cup all-purpose flour, 1/2 cup cornstarch, 2 cups vegetable oil,""In a large bowl, combine the chicken pieces, salt, pepper, garlic powder, onion powder and paprika. Toss until all the chicken pieces are evenly coated. In a separate bowl, mix together the flour and cornstarch. Dip the chicken pieces into the flour mixture and coat them evenly. Heat the oil in a large skillet on medium-high heat. Add the chicken pieces to the skillet and cook for about 10 minutes, or until golden brown and crispy. Remove the chicken from the skillet and serve,"4,15 minutes,25 minutes,Medium,Per Serving: Calories: 556; Fat: 35.4g; Carbohydrates: 24.6g; Protein: 30.2g,Southern,Main Dish'

        chain.columns = "Task ID|Task Description|Priority Level|Due Date|Status|Date Created|Date Completed".split(
            "|"
        )

        content = """
T1|Write report|High|02/07/2020|Incomplete|01/01/2020|
T2|Go to the store|Low|02/10/2020|Completed|01/02/2020|02/05/2020
T3|Clean the house|Medium|02/15/2020|Incomplete|01/03/2020|
T4|Complete online course|High|03/01/2020|Incomplete|01/04/2020|
T5|Read book|Low|02/28/2020|Completed|01/05/2020|02/20/2020"""

        expected = """[{'Task ID': 'T1', 'Task Description': 'Write report', 'Priority Level': 'High', 'Due Date': '2020-02-07', 'Status': 'Incomplete', 'Date Created': '2020-01-01', 'Date Completed': ''}, {'Task ID': 'T2', 'Task Description': 'Go to the store', 'Priority Level': 'Low', 'Due Date': '2020-02-10', 'Status': 'Completed', 'Date Created': '2020-01-02', 'Date Completed': '2020-02-05'}, {'Task ID': 'T3', 'Task Description': 'Clean the house', 'Priority Level': 'Medium', 'Due Date': '2020-02-15', 'Status': 'Incomplete', 'Date Created': '2020-01-03', 'Date Completed': ''}, {'Task ID': 'T4', 'Task Description': 'Complete online course', 'Priority Level': 'High', 'Due Date': '2020-03-01', 'Status': 'Incomplete', 'Date Created': '2020-01-04', 'Date Completed': ''}, {'Task ID': 'T5', 'Task Description': 'Read book', 'Priority Level': 'Low', 'Due Date': '2020-02-28', 'Status': 'Completed', 'Date Created': '2020-01-05', 'Date Completed': '2020-02-20'}]"""

        actual = chain.process_content(content)

        # check that actual has no nan values
        assert expected == str(actual)


@pytest.mark.parametrize(
    "input, output",
    [
        ("test", "test"),
        ("test()", "test"),
        ("test(a)", "test"),
        ("test(a, b)", "test"),
        ("test(a, b, c)", "test"),
        ("test(a, b, c, d)", "test"),
        ("test(a, b, c, d, e)", "test"),
        ("test(a, b, c, d, e, f)", "test"),
        ("test(a, b, c, d, e, f, g)", "test"),
        ("test(a, b, c, d, e, f, g, h)", "test"),
        ("test(a, b, c, d, e, f, g, h, i)", "test"),
    ],
)
def test_remove_parenthesis(input, output, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "butler.database.database.DatabaseChain.build",
        lambda *args, **kwargs: "test",
    )
    monkeypatch.setattr(
        "butler.database.database.LLMChain", lambda *args, **kwargs: "test"
    )
    chain = DatabaseChain(prompt="test")
    assert chain.remove_parenthesis(input) == output


def test_add_content(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "butler.database.database.DatabaseChain.build",
        lambda *args, **kwargs: "test",
    )
    monkeypatch.setattr(
        "butler.database.database.LLMChain", lambda *args, **kwargs: "test"
    )
    chain = DatabaseChain(prompt="test")
    chain.add_content()

    assert chain.chains == ["test"]
    assert chain.output_variables == ["content"]


# def test_validate_schema():
#     with open("test_data/database/responses/3.json") as f:
#         response = json.load(f)
#     print(response)


"""
Things to test:
    - prompts are well written
    - check if after each add whether the chain has the content
    - check if the transformation chain is well written
    - test the post processing
    - test the output types and schemas
"""
