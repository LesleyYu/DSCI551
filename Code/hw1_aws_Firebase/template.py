# IMPORT LIBRARIES
import json
import requests
import sys

# Firebase Database URLs (Replace these URLs with your actual Firebase URLs)
DATABASE_URLS = {
    0: "URL 1",
    1: "URL 2"
}

## Define any global methods
# HERE


def add_book(book_id, book_json):
    # INPUT : book id and book json from command line
    # RETURN : status code after pyhton REST call to add book [response.status_code]
    # EXPECTED RETURN : 200
    return

def search_by_author(author_name):
    # INPUT: Name of the author
    # RETURN: JSON object having book_ids as keys and book information as value [book_json] published by that author  
    # EXPECTED RETURN TYPE: {'102': {'author': ... , 'price': ..., 'title': ..., 'year': ...}, '104': {'author': , 'price': , 'title': , 'year': }}
    return

def search_by_year(year):
    # INPUT: Year when the book published
    # RETURN: JSON object having book_ids as key and book information as value [book_json] published in that year
    # EXPECTED RETURN TYPE: {'102': {'author': ... , 'price': ..., 'title': ..., 'year': ...}, '104': {'author': , 'price': , 'title': , 'year': }}
    return

# Use the below main method to test your code
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py [operation] [arguments]")
        
    operation = sys.argv[1].lower()
    if operation == "add_book":
        result = add_book(sys.argv[2], sys.argv[3])
        print(result)
    elif operation == "search_by_author":
        books = search_by_author(sys.argv[2])
        print(books)
    elif operation == "search_by_year":
        year = int(sys.argv[2])
        books = search_by_year(year)
        print(books)
