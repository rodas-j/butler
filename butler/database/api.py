from butler.database.database import DatabaseChain
import json


def generate_response(output: DatabaseChain) -> dict:

    js_reponse = {
        "prompt": output.prompt,
        "title": output.output.get("table_metadata", {}).get("Title", "Untitled"),
        "description": output.output.get("table_metadata", {}).get("Description", ""),
        "icon": {
            "type": "emoji",
            "emoji": output.output.get("table_metadata", {}).get("Emoji", "default"),
        },
        "properties": output.output.get("js_objects"),
        "content": output.output.get("content_json", []),
    }
    validate_schema(js_reponse)
    return js_reponse


def validate_schema(response: dict):
    import jsonschema

    with open("tests/test_data/database/responses/schema.json") as f:
        schema = json.load(f)
    jsonschema.validate(response, schema)
