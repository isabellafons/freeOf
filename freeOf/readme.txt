README 

Description: 
Project Name: Free Of Food Allergy Detector
What it Does: Free Of Food Allergy Detector allows a user to scan a food barcode and input their allergens, and It will tell them if they are allergic to it or not. If someone is allergic to a product, it comes up with similar products that they aren’t allergic to and a picture. When you click on the picture it takes you to a link where you can buy the product. If a product isn’t found, a user can type in the product ingredients and it will check from that list.

How to run the project:
The images must be in a file named “images”.This folder MUST be placed in the same file as all the code.  Products.csv is a file from the USDA that MUST be in the same folder as all the code. It is incredibly important that these are in the same folder. Run just the __init__.py file. 

Libraries used (these MUST all be imported):

Below is what you would need to install through your terminal! 
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap homebrew/science
brew install opencv
brew install zbar
pip install pyzbar
pip install imutils
pip install requests
pip install pillow
pip install numpy
pip install beautifulsoup4

In each file, this is what is imported at the top.

webscraping.py
From bs4 import BeautifulSoup
Requests
re

reccommend.py
Webscraping

csvToDict.py
Csv

barcodeScannerVideo.py
From imutils.video import VideoStream
From pyzbar import pyzbar
Argparse
Datetime
Inutils
Time
Cv2
numpy as np
Urllib.request
From urllib.request import Request, url open

init.py
Os
Webscraping
Io
Base64
Inutils
Webbrowser
numpy as np
Urllib
Cv2
From PIL import Image, ImageTk
From url lib.request import urlopen

Shortcut commands: None




