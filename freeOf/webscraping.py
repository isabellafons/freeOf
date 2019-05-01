######## The Webscraping File! This contains the webscraping used to get images and store links! ########


from bs4 import BeautifulSoup
import requests
import re

###Used Webscraping Tutorial from https://www.dataquest.io/blog/web-scraping-beautifulsoup/###
###link webscraping from https://pythonspot.com/extract-links-from-webpage-beautifulsoup/ ###

def getImage(barcode):
    url = "https://www.barcodelookup.com/" + barcode
    
    response = requests.get(url)
    
    html_soup = BeautifulSoup(response.text,'html.parser')
    
    
    image_containers = html_soup.find_all('div', id= "images")
    #print(image_containers)
    
    image_containers = str(image_containers)
    
    image_containers=image_containers.split("src")
    
    #cleanupImageLink
    image_str = ""
    imgLink = (((str(image_containers[-1]).split("="))[-1]).split('"'))[1]

    return imgLink
    
    
def getStoreLink(barcode):
    url = "https://www.barcodelookup.com/" + barcode
    
    response = requests.get(url)
    
    html_soup = BeautifulSoup(response.text,'html.parser')
    
    links = []
    
    
    store_containers = html_soup.find_all('div', class_= "store-list")
    
    
    for link in html_soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
    
    if(links!=[]):
        return links[0]
    else: return None


def getImage2(barcode):
    url = "https://www.barcodespider.com/070221009359"
    
    response = requests.get(url)
    
    html_soup = BeautifulSoup(response.text,'html.parser')
    
    
    image_containers = html_soup.find_all('div', id= "images")
    print(image_containers)
    
    image_containers = str(image_containers)
    
    image_containers=image_containers.split("src")
    
    #cleanupImageLink
    image_str = ""
    imgLink = (str(image_containers[-1]))

    return imgLink
    
    

    
    
