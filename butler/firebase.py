import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from logger import logger

cred = credentials.Certificate(
    "butler/pybutler-firebase-adminsdk-e88bw-363bb47622.json"
)

databaseURL = "https://pybutler-default-rtdb.firebaseio.com/"
try:
    firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})
    ref = db.reference("/database")
except Exception as e:
    logger.error(e)


def pullFromFirebase():
    return ref.get()  # type: ignore


def pushToFirebase(jsonData: dict):
    return ref.push(jsonData)  # type: ignore


if __name__ == "__main__":
    print(type(pullFromFirebase()))
