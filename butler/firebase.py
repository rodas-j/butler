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


def pushToFirebase(jsonData: dict):
    return ref.push(jsonData)  # type: ignore


if __name__ == "__main__":
    test_data = {
        "statement": "I love bird watching. Make me something",
        "types": "Title, Text, Number, Select, Multi-select, Status, Date, Person, Files & media, Checkbox, URL, Email, Phone",
        "result": "\n1. Activity (bird watching)\n2. Frequency (how often they do it)\n3. Location (where they do it)\n4. Duration (how long they do it for)\n5. Equipment (what tools they use)\n6. Species (what birds they observe)\n7. Date/Time (when they do it)",
        "property_types": "\n2. Frequency (how often they do it): Select\n\n3. Location (where they do it): Text\n\n4. Duration (how long they do it for): Number\n\n5. Equipment (what tools they use): Multi-select\n\n6. Species (what birds they observe): Select\n\n7. Date/Time (when they do it): Date",
        "options": " Monthly, Weekly, Daily, Annually, Bi-Annually\n        Equipment: Binoculars, Telescope, Camera, Notebook, Bird Guide\n        Species: Blue Jay, Great Horned Owl, American Robin, Red-tailed Hawk, Warbler",
        "content": "\n        Bird Watching,Weekly,Reedy Creek Nature Preserve,4 Hours,Telescope,American Robin,4/20/2020 10:00 AM\n        Bird Watching,Weekly,The Arboretum,4 Hours,Binoculars,Mourning Dove,4/25/2020 10:00 AM\n        Bird Watching,Monthly,Topsail Hill Preserve State Park,3 Hours,Telescope,Red-tailed Hawk,5/10/2020 10:00 AM\n        Bird Watching,Monthly,Everglades National Park,3 Hours,Binoculars,White Ibis,5/15/2020 10:00 AM\n        Bird Watching,Yearly,Big Cypress National Preserve,5 Hours,Telescope,Brown Pelican,6/1/2020 10:00 AM",
        "details": "\n\nTitle: Bird Watching Log\nDescription: Track your bird watching sessions, including the species you observe, the locations and times you visit, and the tools you use.\nEmoji: 🐦",
    }
    pushToFirebase(test_data)
