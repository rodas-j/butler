from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY = os.environ.get("OPENAI_API_KEY")


llm = OpenAI(
    temperature=0.7,
    openai_api_key=OPEN_AI_API_KEY,
    verbose=True,
)


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

COLORS = [
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

propertyNotation.update({v: v for _, v in propertyNotation.items()})
