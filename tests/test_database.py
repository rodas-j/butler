from pytest import MonkeyPatch
from butler.database.database import DatabaseChain, LLMChain
from unittest.mock import MagicMock, Mock
import unittest.mock as mock
import pytest


monkeypatch = MonkeyPatch()
monkeypatch.setattr(
    "butler.database.database.DatabaseChain.build", lambda *args, **kwargs: "test"
)
monkeypatch.setattr("langchain.chains.llm.LLMChain", lambda *args, **kwargs: "test")


def test_database_chain():

    chain = DatabaseChain(prompt="test")

    assert chain.build() == "test"


def test_add_columns(monkeypatch: MonkeyPatch):
    with mock.patch("butler.database.database.LLMChain") as mock_LLMChain:
        mock_LLMChain.return_value = "test"
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
        ("test(a, b, c, d, e, f, g, h, i, j)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l, m)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l, m, n)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q)", "test"),
        ("test(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r)", "test"),
    ],
)
def test_remove_parenthesis(input, output):
    chain = DatabaseChain(prompt="test")
    assert chain.remove_parenthesis(input) == output


def test_add_content():
    with mock.patch("butler.database.database.LLMChain") as mock_LLMChain:
        mock_LLMChain.return_value = "test"
        chain = DatabaseChain(prompt="test")
        chain.add_content()

        assert chain.chains == ["test"]
        assert chain.output_variables == ["content"]
