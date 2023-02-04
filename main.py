from logger import logger
import os
from flask import Flask, request
from butler.app import queryOpenAI
from butler.database.database import DatabaseChain
from butler.database.api import generate_response
from butler.firebase import FirebaseError, pushToFirebase


class DatabaseError(Exception):
    pass


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


@app.route("/beta/database", methods=["POST"])
def beta_database():

    try:

        message = request.json["message"]
        output = DatabaseChain(prompt=message)
        res = generate_response(output)

    except KeyError as e:
        logger.error(e)
        logger.error("Could not find message in request")
        return {"error": "Could not find message in request"}, 400
    except Exception as e:
        logger.error(e)
        return {"error": "Could not generate response"}, 500

    try:
        pushToFirebase(output.output)
    except FirebaseError as e:
        logger.error(e)
        logger.error("Could not push to Firebase")

    return res


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
