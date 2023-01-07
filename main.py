import os
import sys
from flask import Flask, request
from butler.app import queryOpenAI
from butler.database.database import DatabaseChain
from butler.database.api import generate_response
from butler.firebase import pushToFirebase

app = Flask(__name__)


logs_file_path = "./app.log"

sys.stdout = open(logs_file_path, "w", buffering=1, encoding="utf-8")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# create /database endpoint with a POST request that takes in a message
@app.route("/database", methods=["POST"])
def database():
    message = request.json["message"]
    return queryOpenAI(message)
    # return queryOpenAI(message)


@app.route("/beta/database", methods=["POST"])
def beta_database():
    message = request.json["message"]
    output = DatabaseChain(prompt=message)
    res = generate_response(output)
    pushToFirebase(output.output)
    return res


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
