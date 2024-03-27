# IMPORT LIBRARIES
import json
import requests
import sys

# Firebase Database URLs (Replace these URLs with your actual Firebase URLs)
DATABASE_URLS = {
    0: "https://dsci551-hw1-db1-default-rtdb.firebaseio.com/",
    1: "https://dsci551-hw1-db2-default-rtdb.firebaseio.com/"
}

## Global methods
# input error handling
def is_book(my_book):
    # check if the input is a valid json object
    try:
        book = json.loads(my_book)
    except ValueError as e:
        return 1
    
    # check if the author exists and is a string
    try:
        isString = isinstance(book['author'], str)
        if not isString: return 2
    except KeyError as e:
        return 2
    
    # check if the title exists and is a string
    try:
        if not isinstance(book['title'], str): return 3
    except KeyError as e:
        return 3
    
    # check if the year exists. Year can be either integer or string(e.g. unknown)
    try:
        isString = isinstance(book['year'], str) or isinstance(book['year'], int)
        if (isString == False): return 4
    except KeyError as e:
        return 4
    
    # check if the price exists, and is a number
    try:
        isNumber = isinstance(book['price'], int) or isinstance(book['price'], float)
        if not isNumber: return 5
    except KeyError as e:
        return 5

    return 0

# hash function implementation
def my_hash(author):
    # get the ascii value of each char then sum up
    asc_sum = 0
    for c in author:
        asc_sum = asc_sum + ord(c)
    # print(asc_sum)
    return asc_sum % 2             # assign the hash result into either 0 or 1
    

def add_book(book_id, book_json):
    # INPUT : book id and book json from command line
    # RETURN : status code after pyhton REST call to add book [response.status_code]
    # EXPECTED RETURN : 200

    # handling book_json input errors
    is_book_res = is_book(book_json)
    if (is_book_res == 1): 
        return "Please enter valid json object."
    elif(is_book_res == 2):
        return "Please enter valid book author."
    elif(is_book_res == 3):
        return "Please enter valid book title."
    elif(is_book_res == 4):
        return "Please enter valid book year."
    elif(is_book_res == 5):
        return "Please enter valid book price."
    
    my_book = json.loads(book_json)     # reads json into a python dictionary
    db_id = my_hash(my_book["author"])

    # accessing the database
    # check if the book_id already exists
    res1 = requests.get(DATABASE_URLS[db_id]+"books/"+book_id+".json")
    # print(res1.ok)  # returns True. But the result is "null". It's not the `book_is.json.`data. It's the whole database with "null" value in it.
    # if exists, check for replacement confirmation
    if ("author" in res1.text):
        confirmation = input("This entry already exists. Are you aure you want to update it? (yes/no)\n")
        if (confirmation == "no" or confirmation == "n"):
            return "You did not update the entry. Process finished."
        elif (confirmation == "yes" or confirmation == "y"):
            response = requests.patch(DATABASE_URLS[db_id]+"books/"+book_id+".json", book_json)
        else:
            return "Please enter yes or no."
    # if doesn't exist, use put method to write data
    else:
        response = requests.patch(DATABASE_URLS[db_id]+"books/"+book_id+".json", book_json)
    return response

def search_by_author(author_name):
    # INPUT: Name of the author
    # RETURN: JSON object having book_ids as keys and book information as value [book_json] published by that author  
    # EXPECTED RETURN TYPE: {'102': {'author': ... , 'price': ..., 'title': ..., 'year': ...}, '104': {'author': , 'price': , 'title': , 'year': }}

    db_id = my_hash(author_name)
    response = requests.get(DATABASE_URLS[db_id]+'books.json?orderBy="author"&equalTo="'+author_name+'"')
    if (author_name in response.text):
        return response.text
    else: 
        return "The author is not found. Please try again."

def search_by_year(year):
    # INPUT: Year when the book published
    # RETURN: JSON object having book_ids as key and book information as value [book_json] published in that year
    # EXPECTED RETURN TYPE: {'102': {'author': ... , 'price': ..., 'title': ..., 'year': ...}, '104': {'author': , 'price': , 'title': , 'year': }}
    resp1 = requests.get(DATABASE_URLS[0]+'books.json?orderBy="year"&equalTo='+str(year))
    resp2 = requests.get(DATABASE_URLS[1]+'books.json?orderBy="year"&equalTo='+str(year))
    val1 = resp1.text.strip('{''}')
    val2 = resp2.text.strip('{''}')
    return ("{" + val1 + val2 + "}")


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
