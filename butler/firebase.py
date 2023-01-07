import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    "butler/pybutler-firebase-adminsdk-e88bw-363bb47622.json"
)

databaseURL = "https://pybutler-default-rtdb.firebaseio.com/"
firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})


ref = db.reference("/")


def pushToFirebase(jsonData: dict):
    return ref.push(jsonData)  # type: ignore
