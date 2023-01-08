import re
from typing import List


def get_columns_from_text(text):
    regex = r"\d. (.*)"
    extract = re.findall(regex, text)
    # strip whitespace
    extract: List[str] = [x.strip() for x in extract]
    return extract


def get_properties_from_details(text):
    regex = r"(.+): (.*)"
    extract = re.findall(regex, text)
    # strip whitespace
    extract = [(x[0].strip(), x[1].strip()) for x in extract]
    return extract


def main():
    text = """
    1. Goal Name 
2. Goal Description 
3. Start Date 
4. End Date 
5. Status 
6. Progress 
7. Notes 
8. Priority Level 
9. Time Spent 
10. Resources Used
"""
    print(", ".join(get_columns_from_text(text)))


if __name__ == "__main__":
    main()
