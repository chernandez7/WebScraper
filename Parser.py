from bs4 import BeautifulSoup
from threading import Thread
from multiprocessing import Queue
import time
import requests

start = time.time()

url_queue = Queue(100)

#Creating and opening file
file = open("data.txt", "w+")
file.write("{:40} {:15} {:14}\n".format("Name", "Count", "Price"))

def worker():
    '''Gets the next url from the queue and processes it'''
    while True:
        #URL Requests
        url = url_queue.get()
        print ("Processing '{}'...".format(url))
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
                file.write("\t".join(map(str, list_of_cells)).strip()+ "\n")

        url_queue.task_done()

#Creating a pool of workers
for i in range(20):
    t = Thread(target = worker)
    t.daemon = True
    t.start()
        
#4345 Pages to run in the site
urllist = ["http://ragial.com/search/iRO-Renewal//{}".format(str(pgnum)) for pgnum in range(1, 4345+1)]
for url in urllist:
    url_queue.put(url)

#Block until everything is finished
url_queue.join()

file.close()
end = time.time()
print ("Finished in {} seconds".format(str(end - start)))
