"""
Program to automatically download all pages from web book in txt file and then convert it to .doc
BE SURE to leave the PC in 'EN' as language mode

Change the web site on row 18 and 19
Change the name of the output file on row 21

"""
import requests  # downloads content
import bs4  # a module for extracting information from an HTML page
from datetime import datetime  # only to calculate the duration of the program

import subprocess  # to open OpenOffice Writer and convert to .doc
import time  # to make some delays
import pyautogui  # to simulate keyboard keys when saving the file in OO Writer

# declare the url
url_main = 'http://www.manybooks4u.com/Classics/'
url_ext = 'e6031.html'
url = url_main + url_ext  # After You
file_to_convert = "D:\SoftUni\Python\myProjects\webdownloader\output\Jojo\AfterYou_MeBeforeYou2.txt"
book_file = open(file_to_convert, "a")

print("Saving downloaded content to .txt file...")

while not url.endswith('#'):  # url ends with # at the last Next link
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
    title = str(book.select('h1'))
    author = str(book.select('h3'))
    text = book.select('p')  # select all book text in the page (check page info for CSS format elements)
    parag_to_save = []
    # since the last paragraph is an advertisment -
    # create a list with all paragraphs in the page,
    # determine its length
    # and substract the element on the last position
    for parag in text:
        parag_to_save.append(parag)
    final_parag = int(len(parag_to_save) - 1)  # estimate the last paragraph to be saved

    # save the information to a file
    text_to_save = str(parag_to_save[0:final_parag])
    try:
        book_file.write(str(title))
        book_file.write(str(author))
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
            url = url_main + nextLink
book_file.close()

time.sleep(10)

print("Converting to .doc. Please do not use the PC during this conversion")
subprocess.Popen(["C:\Program Files\OpenOffice 4\program\swriter.exe", file_to_convert])

time.sleep(10)

# confirm the encoding when opening .txt in OpenOffice
pyautogui.press('enter', interval=1)
pyautogui.PAUSE = 5  # wait a bit for the file to load

# find and replace paragraph symbols
pyautogui.hotkey('ctrl', 'f')  # open "Find and replace"
pyautogui.typewrite("</p>, <p>")
pyautogui.press(['tab', ' ', 'tab', 'tab', 'tab', 'tab', 'enter'])  # find and replace all
pyautogui.press('enter')
pyautogui.press('c')
pyautogui.PAUSE = 2  # wait a bit

# Save the file as .doc
pyautogui.hotkey('ctrl', 'shift', 's')  # select "Save as..."
pyautogui.PAUSE = 2  # wait a bit
pyautogui.press(['tab', 'down', 'm', 'm', 'enter', 'enter'])  # select .doc extension and save
pyautogui.press('y')  # just in case the file exists - it will be overwritten

# close the file
pyautogui.hotkey('ctrl', 'q')
pyautogui.press('enter')

endtime = datetime.now()
totaltime = endtime - starttime
print("Total time to download and convert: " + str(totaltime))
