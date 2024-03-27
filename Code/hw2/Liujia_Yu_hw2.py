# IMPORT LIBRARIES
import sys
import json
from lxml import etree

# Define any helper functions here
# hash function implementation
def my_hash(author):
    # get the ascii value of each char then sum up
    asc_sum = 0
    for c in author:
        asc_sum = asc_sum + ord(c)
    return asc_sum % 2         # assign the hash result into either 0 or 1
    

def add_book(book_id, book_json):
    # INPUT : book json from command line
    # RETURN : 1 if successful, else 0
    # Assume JSON is well formed with no missing attributes
    my_book = json.loads(book_json)     # reads json into a python dictionary
    db_id = my_hash(my_book["author"])

    # accessing the database
    try:
        tree = etree.parse(XML_FILES[db_id])
    except etree.ParseError:
        # writing default and root elements into empty xml file.
        bib = etree.Element("bib")
        default_element = etree.Element("cd")
        default_element.text = "abc"
        bib.append(default_element)
        tree = etree.ElementTree(bib)
        tree.write(XML_FILES[db_id], pretty_print=True)

    # writing id(as attrib) and four sub-elements into bib/book
    tree = etree.parse(XML_FILES[db_id])
    # print(etree.tostring(tree))     # test
    bib = tree.getroot()     # get the root element 'bib' to write back into xml    # print(bib)
    
    # if book_id already exists, return 0 (fail)
    if (not tree.xpath(f'//book[@id={book_id}]/title/text()') == []):
        return 0
    # else continue with adding the book
    book = etree.SubElement(bib, "book", id=book_id)
    author = etree.SubElement(book, "author")
    author.text = my_book["author"]
    title = etree.SubElement(book, "title")
    title.text = my_book["title"]
    year = etree.SubElement(book, "year")
    year.text = str(my_book["year"])
    price = etree.SubElement(book, "price")
    price.text = str(my_book["price"])
    tree.write(XML_FILES[db_id], pretty_print=True)
    
    # test if written successfully
    tree = etree.parse(XML_FILES[db_id])
    if ((my_book["title"]) in str(tree.xpath('//title/text()'))):
        return 1
    else:   return 0

def search_by_author(author_name):
    # INPUT: name of author
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book title 1', 'book title 2', ...]
    db_id = my_hash(author_name)
    tree = etree.parse(XML_FILES[db_id])
    return tree.xpath(f'/bib/book[author="{author_name}"]/title/text()')

def search_by_year(year):
    # INPUT: year of publication
    # RETURN: list of strings containing only book titles
    # EXPECTED RETURN TYPE: ['book name 1', 'book name 2', ...]
    tree0 = etree.parse(XML_FILES[0])
    tree1 = etree.parse(XML_FILES[1])
    booksIn0 = tree0.xpath(f"/bib/book[year={year}]/title/text()")
    booksIn1 = tree1.xpath(f"/bib/book[year={year}]/title/text()")
    return booksIn0 + booksIn1

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
