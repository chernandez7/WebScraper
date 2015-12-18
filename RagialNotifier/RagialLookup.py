from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import threading
import sys
import subprocess
import requests

#Initialization of variables
url_queue = Queue(100)
search_word = sys.argv[1]

#Worker class that threads run
def worker():
    while True:
        #URL Requests
        url = url_queue.get()
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")

        #Populating arrays of a single page
        list_of_rows = []
        for row in table.findAll("tr")[1:]:
            list_of_cells = []
            for cell in row.findAll("td"):
                for a in cell.findAll("td"):
                    list_of_cells.append(name)
                list_of_rows.append(cell.text)
                
        itemprice = list_of_rows[2][:-1]
        itemprice = int(itemprice.replace(",", ""))

        #Executing ahk script under certain parameters
        if (itemprice < 600000):
            args = [r"TextNotifier.exe", "{}: selling at less than 600,000!".format(search_word)]
            subprocess.call(args)
        elif (itemprice < 650000):
            args = [r"TextNotifier.exe", "{}: selling at less than 650,000!".format(search_word)]
            subprocess.call(args)
        elif (itemprice < 700000):
            args = [r"TextNotifier.exe", "{}: selling at less than 700,000!".format(search_word)]
            subprocess.call(args)
        
        #Job complete
        url_queue.task_done()

#Thread-Safe iteration of a number
def safe_iterate(number):
    number += 1
    return number

#Creating a pool of workers
for i in range(1):
    t = Thread(target = worker)
    t.daemon = True
    t.start()
        
#Adds search to queue
searchurl = "http://ragial.com/search/iRO-Renewal/{}".format(search_word)
url_queue.put(searchurl)

#Block until everything is finished
url_queue.join()
