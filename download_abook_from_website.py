"""
Program to automatically download all pages from web book

Change the web site on row 11
Change the name of the output file on row 15

"""
import requests #downloads content
import bs4 # a module for extracting information from an HTML page
from datetime import datetime #only to calculate the duration of the program

# declare the url
url = 'http://www.manybooks4u.com/Fantasy/e4779.html' #(LiveshipTraders #3) by Robin Hobb

book_file = open("LT3 - ShipOfDestiny.txt", "a")

while not url.endswith('#'): # url ends with # at the last Next link
    starttime = datetime.now()
    # pass the downloaded page to BeautifulSoup
    res = requests.get(url)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    book = bs4.BeautifulSoup(res.text, "html.parser")
    print("Downloading contents from " + url)
    # use BS4 methods to find specific information in a page
    text = book.select('p') # select all book text in the page (check page info for CSS format elements)
    parag_to_save = []
    # since the last paragraph is an advertisment -
    # create a list with all paragraphs in the page,
    # determine its length
    # and substract the element on the last position
    for parag in text:
        parag_to_save.append(parag)
    final_parag = int(len(parag_to_save)-1) #estimate the last paragraph to be saved

    # save the information to a file
    text_to_save = str(parag_to_save[0:final_parag])
    try:
        book_file.write(text_to_save)
    except Exception as exc:
        print('There was a problem: %s' % (exc))

# find the Next link

# find all links and export to a list
    allLinks = book.find_all('a')

# check if Next exists in an element from allLinks -> get the url for the nextLink
    for link in allLinks:
        if "Next" in link:
            nextLink = link.get('href')
            url = 'http://www.manybooks4u.com/Fantasy/' + nextLink
book_file.close()
endtime = datetime.now()
totaltime = endtime - starttime
print("Total time to download: " + str(totaltime))