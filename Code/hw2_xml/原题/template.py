# IMPORT LIBRARIES
import sys
import json
from lxml import etree

# Define any helper functions here


def add_book(book_id, book_json):
    # INPUT : book json from command line
    # RETURN : 1 if successful, else 0 
    # Assume JSON is well formed with no missing attributes
    return

def search_by_author(author_name):
    # INPUT: name of author
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book title 1', 'book title 2', ...]
    return 

def search_by_year(year):
    # INPUT: year of publication
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book name 1', 'book name 2', ...]
    return 

# Use the below main method to test your code
if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit("\nUsage: python3 script.py [path/to/file0.xml] [path/to/file1.xml] [operation] [arguments]\n")

    xml0, xml1 = sys.argv[1], sys.argv[2]

    # Assume XML files exist at mentioned path and are initialized with empty <bib> </bib> tags
    global XML_FILES 
    XML_FILES = {
        0: xml0,
        1: xml1
    }

    operation = sys.argv[3].lower()

    if operation == "add_book":
        result = add_book(sys.argv[4], sys.argv[5])
        print(result)
    elif operation == "search_by_author":
        books = search_by_author(sys.argv[4])
        print(books)
    elif operation == "search_by_year":
        year = int(sys.argv[4])
        books = search_by_year(year)
        print(books)
    else:
        sys.exit("\nInvalid operation.\n")
