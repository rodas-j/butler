import json
from typing import List
from pytest import MonkeyPatch

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
