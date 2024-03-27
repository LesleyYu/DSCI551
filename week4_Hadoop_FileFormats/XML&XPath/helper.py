
from lxml import etree

def printf(elems):
    if (isinstance(elems, list)):
        for elem in elems:
            if isinstance(elem, str):
                print(elem)
            else:
                print(etree.tostring(elem).decode('utf-8'))
    else: # just a single element
        print(etree.tostring(elems).decode('utf-8'))
