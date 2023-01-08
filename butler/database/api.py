from butler.database.database import DatabaseChain


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
        "content": output.output.get("content_json"),
    }
    return js_reponse
