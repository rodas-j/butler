from langchain.llms import OpenAI


llm = OpenAI(
    temperature=0.7,
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
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


propertyNotation.update({v: v for _, v in propertyNotation.items()})
