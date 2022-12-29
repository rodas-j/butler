import os
from flask import Flask, request
from butler.app import queryOpenAI

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# create /database endpoint with a POST request that takes in a message
@app.route("/database", methods=["POST"])
def database():
    message = request.json["message"]
    return queryOpenAI(message)
    # return queryOpenAI(message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
