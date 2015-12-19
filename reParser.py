from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import threading
import sys
import urllib.request
import os
import time
import requests

#Initialization of variables
start = time.time()
lock = threading.Lock()
url_queue = Queue(100)
item_count = 0
chapter_number = 57

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
        foldername = url[57:-5]
        create_folder(foldername)

        #Populating arrays of a single page
        list_of_images = []
        for img in soup.find_all("img")[5:len(soup.find_all("img"))-22]:
            list_of_images.append(img["src"])
            item_count = safe_iterate(item_count)

        #add method to get image and put in folder
        for url in list_of_images:
            filename =  os.path.normpath("C:/Users/Chris/Documents/Tokyo Ghoul RE/{}/".format(foldername) + url[len(url)-6:])
            urllib.request.urlretrieve(url, filename)
            
        url_queue.task_done()

#Thread-Safe iteration of a number
def safe_iterate(number):
    number += 1
    return number

#Creates folder
def create_folder(name):
    newpath = os.path.normpath("C:/Users/Chris/Documents/Tokyo Ghoul RE/{}".format(name))
    if not os.path.exists(newpath):
        os.makedirs(newpath)

#Creating a pool of workers
for i in range(10):
    t = Thread(target = worker)
    t.daemon = True
    t.start()
        
#Gets all the url's for each chapter
urllist = []
starturl = "http://www.bimanga.com/2015/05/read-manga-tokyo-ghoul-re-chapter-01.html"
response = requests.get(starturl)
html = response.content
soup = BeautifulSoup(html, "html.parser")
soup.prettify()
body = soup.find_all('select',name='menu') ########FIX
#for divider in body.findAll('div'):
    #for select in divider.findAll('select', value=True):
print (body)
        
#for option in body.find('option'):
    #urllist.append(option["value"])
 #   print(option['value'])

for url in urllist:
    url_queue.put(url)
    
#Block until everything is finished
url_queue.join()

end = time.time()
print ("Finished processing {} items in {} seconds".format(str(item_count), str(end - start)))
