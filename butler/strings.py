# DATABASES
from butler.utils import get_properties_from_details


DATABASE_BASIC_PROPERTIES = """
Title: Whatever you're calling your item, i.e. the title of the page in your database.

Text: Basic text for notes, descriptions and comments about database items.

Number: Numerical formats like currencies and percentages. Useful for price, etc.

Select: Dropdown menu of tags that can be selected one at a time.

Multi-select: Dropdown menu of tags letting you add more than one at a time.

Status: Dropdown menu of tags that are grouped by status (i.e. To-do, In Progress, Complete). Learn more about the Status property →

Date: Accepts a date or a date range, allowing you to timestamp and set reminders.

Person: Lets you mention other users in your workspace (or assign them to things).

Files & media: Allows you to upload files relevant to your database item.

Checkbox: Simple checkboxes that indicate whether something is done or not.

URL: Accepts a link to a website relevant to your database item.

Email: Accepts email addresses and launches your mail client when clicked.

Phone: Accepts a phone number and prompts your phone or computer to call it when clicked.
"""

ADVANCED_PROPERTIES = """
Formula: Lets you perform calculations or trigger actions based on other properties. 

Relation: Lets you add items from another database as a property. 

Rollup: Runs calculations based on properties in a related database.

Created time: Timestamps an item's creation.

Created by: Automatically records the user who created the item.

Last edited time: Timestamps an item's last edit.

Last edited by: Records the user who edited the item last.
"""


def main():
    # list the basic property names
    names = [x[0] for x in get_properties_from_details(DATABASE_BASIC_PROPERTIES)]
    print(", ".join(names))


if __name__ == "__main__":
    main()
