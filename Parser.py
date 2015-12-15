from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import threading
import sys
import time
import requests

#Initialization of variables
start = time.time()
lock = threading.Lock()
number_lock = threading.Lock()
url_queue = Queue(100)
item_count = 0

#Creating and opening file
file = open("data.txt", "w+")
file.write("{:40} {:15} {:14}\n".format("Name", "Count", "Price"))

#Worker class that threads run
def worker():
    '''Gets the next url from the queue and processes it'''
    global item_count
    while True:
        #URL Requests
        url = url_queue.get()
        sys.stdout.write("Processing '{}'...\n".format(url))
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
                list_of_cells.append(cell.text)
                
            #Writing to file
            item_count = safe_iterate(item_count)
            safe_write_to_file(list_of_cells)
        url_queue.task_done()

#Thread-Safe form of writing to file
def safe_write_to_file(input):
    lock.acquire()
    file.write("\t".join(map(str, input)).strip()+ "\n")
    lock.release()

#Thread-Safe iteration of a number
def safe_iterate(number):
    number_lock.acquire()
    number += 1
    number_lock.release()
    return number

#Creating a pool of workers
for i in range(10):
    t = Thread(target = worker)
    t.daemon = True
    t.start()
        
#4345 Pages to run in the site
urllist = ["http://ragial.com/search/iRO-Renewal//{}".format(str(pgnum)) for pgnum in range(1, 4345+1)]
#urllist = ["http://ragial.com/search/iRO-Renewal//{}".format(str(pgnum)) for pgnum in range(1, 100+1)]
for url in urllist:
    url_queue.put(url)

#Block until everything is finished
url_queue.join()

file.close()
end = time.time()
print ("Finished processing {} items in {} seconds".format(str(item_count), str(end - start)))
