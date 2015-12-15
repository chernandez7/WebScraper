import time
import csv
import requests
from bs4 import BeautifulSoup

start = time.time()

#4345 Pages to run in the site
#url = ["http://ragial.com/search/iRO-Renewal//{}".format(str(pgnum)) for pgnum in range(1, 4345+1)]
#print ("\n".join(url))

#for loop start

url = "http://ragial.com/search/iRO-Renewal//"
print ("Processing {}...".format(url))
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "html.parser")

table = soup.find("table") #no attrs needed because of ragial format

list_of_rows = []
for row in table.findAll("tr")[1:]:
    list_of_cells = []
    for cell in row.findAll("td"):
        for a in cell.findAll("td"):
            name = cell.text.strip(" ")
            index = name.find("x")
            name = name[:index]
            list_of_cells.append(name)
        list_of_cells.append(cell.text)
    list_of_rows.append(list_of_cells)
print (list_of_rows)


#outfile = open("./parser.csv", "wb")
#writer = csv.writer(outfile)
#writer.writerow({"Name", "Count", "Price", "Discount?"})
#writer.writerows(list_of_rows)

end = time.time()
print ("Finished in {} seconds".format(str(end - start)))
