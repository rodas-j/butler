import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from logger import logger


class FirebaseError(Exception):
    pass


cred = credentials.Certificate(
    "PATH_TO_JSON_FILE"
)

databaseURL = "PATH_TO_DATABASE"
try:
    firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})
except Exception as e:
    logger.error(e)


def pullFromFirebase(ref="database"):
    ref = db.reference("/" + ref)
    return ref.get()  # type: ignore


def pushToFirebase(jsonData: dict, ref="database"):
    try:
        ref = db.reference("/" + ref)
        return ref.push(jsonData)  # type: ignore
    except Exception as e:
        logger.error(e)
        raise FirebaseError("Could not push to Firebase")


if __name__ == "__main__":
    print(type(pullFromFirebase()))
