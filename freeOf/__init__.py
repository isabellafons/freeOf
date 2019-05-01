#### This is the core file of the project and contains basic Animation framework $$$

from tkinter import *
import barcodeScannerVideo
from barcodeScannerVideo import found
import csvToDict
from csvToDict import productDict, nameDict, manuDict
import allergyDetermine
import os
import reccommend
import webscraping
import io
import base64
import imutils
import webbrowser

import numpy as np
import urllib

import cv2

from PIL import Image, ImageTk

from urllib.request import urlopen

####################################
# init #
####################################

####READ BARCODE CSV FROM 15-110 F18 Website #####

# Note: As this requires read-write access to your hard drive,
#       this will not run in the browser in Brython.

def readFile(path):
    # This makes a very modest attempt to deal with unicode if present
    with open(path, 'rt', encoding='ascii', errors='surrogateescape') as f:
        return f.read()

def readCsvFile(path):
    # Returns a 2d list with the data in the given csv file
    result = [ ]
    for line in readFile(path).splitlines():
        result.append(line.split(','))
    return result

def init(data):
    # load data.xyz as appropriate
    data.stateOptions = ["home","allergyCheck","scanner","barcodeCheck","determineSafety","safeFood","unsafeFood","wrongItem","recommend","disclaimer"]
    data.curState = data.stateOptions[0]
    data.image0 = PhotoImage(file = 'images/homeBack.gif')
    data.image1 = PhotoImage(file = 'images/allerInput.gif')
    data.image2 = PhotoImage(file = 'images/scanBack.gif')
    data.image3 = PhotoImage(file = 'images/youScanned.gif')
    data.safeImage = PhotoImage(file = 'images/safeToEatGreen.gif')
    data.unSafeImage = PhotoImage(file = 'images/notSafeRed.gif')
    data.rescanImage = PhotoImage(file = 'images/rescan.gif')
    data.tryTheseImage = PhotoImage(file = 'images/tryThese.gif')
    data.disclaimerImage = PhotoImage(file = 'images/disclaimer.gif')
    data.allergyInput = [["Dairy",False],["Eggs",False],["Gluten",False],["Peanuts",False],["Sesame",False],["Shellfish",False],["Soy",False],["Tree Nuts",False]]
    data.selectedAllergies = set()
    data.barcode = ""
    data.foundBarcode = False
    data.ingList,data.allerList = [],[]
    data.wrongCount = 0
    data.allerText = ""
    data.itemName = ""
    data.inputtingAllergen = False
    data.inputtingIngred = False
    data.customIngredList = False
    data.customAllergen = ""
    data.customIngred = ""
    data.optionalAllergens = set()
    data.reccommendProducts = []
    data.recProductsIndex = 0
    
    #Help Drawing Photo from website URL is from https://www.daniweb.com/programming/software-development/code/440946/display-an-image-from-a-url-tkinter-python#
    data.recImgLink = ""
    data.recPhoto = None
    data.image_byt = None
    data.image_b64 = None
    
    
    
    
########################
# Mode Controllers #
##########################
def mousePressed(event, data):
    # use event.x and event.y
#Home Input Checks
    if(data.curState == "home"):
        homeMousePressed(event,data)
    #Allergy Input Checks
    if(data.curState=="allergyCheck"):
        allergyCheckMousePressed(event,data)
    if(data.curState=="scanner"):
        scannerMousePressed(event,data)
    if(data.curState == "barcodeCheck"):
        barcodeCheckMousePressed(event,data)
    if(data.curState == "wrongItem"):
        wrongItemMousePressed(event,data)
    if(data.curState=="safeFood"):
        safeFoodMousePressed(event,data)
    if(data.curState=="unsafeFood"):
        unSafeFoodMousePressed(event,data)
    if(data.curState=="recommend"):
        recommendMousePressed(event,data)
    if(data.curState=="disclaimer"):
        disclaimerMousePressed(event,data)

        
    if(data.curState!="home" and data.curState!="safeFood" and data.curState!="unsafeFood" and data.curState!="disclaimer"):
        if(event.x>1180 and event.x<1280 and event.y>0 and event.y<40):
            barcodeScannerVideo.found = set()
            data.barcode = ""
            data.optionalAllergens = set()
            data.customAllergen = ""
            data.customIngred = ""
            data.recProductsIndex = 0
            
            for item in data.allergyInput:
                item[1] = False
            data.curState = "home"
        

            
def keyPressed(event, data):
    if(data.curState=="allergyCheck"):
        inputAllergenKeyPressed(event,data)
    if(data.curState == "barcodeCheck"):
        barcodeCheckKeyPressed(event,data)
    
            
                
   
def timerFired(data):
    if(data.curState=="scanner"):
        scannerTimerFired(data)
    if(data.curState=="wrongItem"):
        wrongItemTimerFired(data)

        

def redrawAll(canvas, data):
    # draw in canvas
    if(data.curState=="home"):
        homeScreenRedrawAll(canvas,data)
    if(data.curState=="allergyCheck"):
        allergyCheckRedrawAll(canvas,data)
    if(data.curState=="scanner"):
        scannerRedrawAll(canvas,data)
    if(data.curState=="barcodeCheck") or (data.curState=="determineSafety"):
        barcodeCheckRedrawAll(canvas,data)
    if(data.curState=="safeFood"):
        safeFoodRedrawAll(canvas,data)
    if(data.curState=="unsafeFood"):
        unSafeFoodRedrawAll(canvas,data)
    if(data.curState == "wrongItem"):
        wrongItemRedrawAll(canvas,data)
    if(data.curState == "recommend"):
        recommendRedrawAll(canvas,data)
    if(data.curState=="disclaimer"):
        disclaimerRedrawAll(canvas,data)
        
    #"safeFood","unsafeFood"
    if(data.curState!="home" and data.curState!="safeFood" and data.curState!="unsafeFood" and data.curState!="disclaimer"):
        canvas.create_rectangle(1180,0,1280,40,fill = "white",width = 4,outline ='#a79eff')
        canvas.create_text(1230,20,text = "Home", font = "Helvetica 16 bold italic")
        
        
        
##### modes #####

##################
# home screen mode #
##################

def homeMousePressed(event,data):
    mouseX = event.x
    mouseY = event.y
    
    if(event.x>280 and event.x<1010 and event.y>340 and event.y<500):
        data.curState = data.stateOptions[1]
        print(data.curState)
        
    if(event.x>500 and event.x<780 and event.y>540 and event.y<640):
        data.curState = "disclaimer"

def homeScreenRedrawAll(canvas,data):
        canvas.create_rectangle(0,0,data.width,data.height, fill ="white",width = 0)
        canvas.create_image(0,0, image=data.image0, anchor =NW)
        canvas.create_rectangle(280,340,1010,500,fill = "white",width = 10,outline ='#a79eff')
        canvas.create_text(645,420,text = "Let's Get Started!", font = "Helvetica 46 bold italic")
        
        canvas.create_rectangle(500, 540, 780, 640, fill = "white", width = 5, outline = "#a79eff")
        canvas.create_text(640, 590, text = "Disclaimer", font = "Helvetica 26 bold italic")


#######################
# allergy Check Mode #
#######################


def allergyCheckMousePressed(event,data):
        mouseX = event.x
        mouseY = event.y
        
       #submit button for inputting allergen
        if(event.x>775 and event.x<894 and event.y>490 and event.y<550):
            data.inputtingAllergen = False
            data.optionalAllergens.add(data.customAllergen)
            data.customAllergen = ""
            print("optional Allergens",data.optionalAllergens)
        
        
        #input allergen button
        if(event.x>344 and event.x<754 and event.y>490 and event.y<550):
            data.inputtingAllergen = True
        
        #Dairy
        if(event.x>344 and event.x<374 and event.y>210 and event.y<240):
            data.allergyInput[0][1] = not data.allergyInput[0][1]
        #Egg
        if(event.x>344 and event.x<374 and event.y>280 and event.y<310):
            data.allergyInput[1][1] = not data.allergyInput[1][1]
        #Gluten
        if(event.x>244 and event.x<374 and event.y>350 and event.y<380):
            data.allergyInput[2][1] = not data.allergyInput[2][1]
        #Peanuts
        if(event.x>344 and event.x<374 and event.y>420 and event.y<480):
            data.allergyInput[3][1] = not data.allergyInput[3][1]
        #Sesame
        if(event.x>644 and event.x<674 and event.y>210 and event.y<240):
            data.allergyInput[4][1] = not data.allergyInput[4][1]
        #Shellfish
        if(event.x>644 and event.x<674 and event.y>280 and event.y<310):
            data.allergyInput[5][1] = not data.allergyInput[5][1]
        #Soy
        if(event.x>644 and event.x<674 and event.y>350 and event.y<380):
            data.allergyInput[6][1] = not data.allergyInput[6][1]
        #Tree Nuts
        if(event.x>644 and event.x<674 and event.y>420 and event.y<480):
            data.allergyInput[7][1] = not data.allergyInput[7][1]
            
        #Create Allergen List
        for allergen in data.allergyInput:
            if(allergen[1]==True):
                data.selectedAllergies.add(allergen[0])
            elif(allergen[0] in data.selectedAllergies) and (allergen[1]==False):
                data.selectedAllergies.remove(allergen[0])
        print(data.selectedAllergies)
        
        #Check for moving to next state
        
        if(event.x>244 and event.x<1044 and event.y>620 and event.y<680):
            data.curState = data.stateOptions[2]
                
                
            


def allergyCheckRedrawAll(canvas,data):
        canvas.create_image(0,0,image = data.image1, anchor = NW)
        #Input boxes
        
        #dairy
        canvas.create_text(394,225,text="dairy",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[0][1]==False):
            canvas.create_rectangle(344,210,374,240,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[0][1]==True):
            canvas.create_rectangle(344,210,374,240,fill="#a79eff",width=3, outline = "#a79eff")
        #eggs
        canvas.create_text(394,295,text="eggs",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[1][1]==False):
            canvas.create_rectangle(344,280,374,310,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[1][1]==True):
            canvas.create_rectangle(344,280,374,310,fill="#a79eff",width=3, outline = "#a79eff")
        
        #gluten
        canvas.create_text(394,365,text="gluten",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[2][1]==False):
            canvas.create_rectangle(344,350,374,380,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[2][1]==True):
            canvas.create_rectangle(344,350,374,380,fill="#a79eff",width=3, outline = "#a79eff")
        #peanuts
        canvas.create_text(394,435,text="peanuts",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[3][1]==False):
            canvas.create_rectangle(344,420,374,450,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[3][1]==True):
            canvas.create_rectangle(344,420,374,450,fill="#a79eff",width=3, outline = "#a79eff")
        #sesame
        canvas.create_text(694,225,text="sesame",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[4][1]==False):
            canvas.create_rectangle(644,210,674,240,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[4][1]==True):
            canvas.create_rectangle(644,210,674,240,fill="#a79eff",width=3, outline = "#a79eff")
        #shellfish
        canvas.create_text(694,295,text="shellfish",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[5][1]==False):
            canvas.create_rectangle(644,280,674,310,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[5][1]==True):
            canvas.create_rectangle(644,280,674,310,fill="#a79eff",width=3, outline = "#a79eff")
        #soy
        canvas.create_text(694,365,text="soy",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[6][1]==False):
            canvas.create_rectangle(644,350,674,380,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[6][1]==True):
            canvas.create_rectangle(644,350,674,380,fill="#a79eff",width=3, outline = "#a79eff")
        #tree nuts
        canvas.create_text(694,435,text="tree nuts",font = "Helvetica 46 italic", fill = "#a79eff", anchor = W)
        if(data.allergyInput[7][1]==False):
            canvas.create_rectangle(644,420,674,450,fill="white",width=3, outline = "#a79eff")
        elif(data.allergyInput[7][1]==True):
            canvas.create_rectangle(644,420,674,450,fill="#a79eff",width=3, outline = "#a79eff")
            
        #Type your own allergen box!
        #when u click it it makes method where u can write text!
        canvas.create_rectangle(344,490,754,550, fill = "white", width = 2, outline = "#a79eff")
        canvas.create_rectangle(775,490,894,550, fill = "white", width = 2, outline = "#a79eff")
        canvas.create_text(834,520,text = "Submit!", font = "Helvetica 26 bold italic")
        
        if(data.inputtingAllergen==False):
            canvas.create_text(549,520, text = "Input custom ingredient!", font = "Helvetica 16 bold italic")
            
        if(data.inputtingAllergen==True):
            canvas.create_text(549,520, text = data.customAllergen, font = "Helvetica 16 bold italic")
        
        canvas.create_rectangle(244,620,1044,680,fill = "white", width = 10,outline ='#a79eff')
        canvas.create_text(644,650,text = "Scan your barcode!", font = "Helvetica 26 bold italic")
        
def inputAllergenKeyPressed(event,data):
    if(data.inputtingAllergen==True):
        if(event.keysym=="BackSpace"):
            data.customAllergen = data.customAllergen[:-1]
        elif(event.keysym=="space"):
            data.customAllergen+=" "
        else:
            data.customAllergen += event.keysym
    
    
    
    
    

#####################
# scan back mode #
#####################
        
def scannerRedrawAll(canvas,data):
    canvas.create_image(0,0,image=data.image2,anchor=NW)
    allergyStr = ""
    for allergen in data.selectedAllergies:
        allergyStr += str(allergen)
        allergyStr += ","
    if(data.optionalAllergens!=None):
        for allergen2 in data.optionalAllergens:
            allergyStr += str(allergen2)
            allergyStr += ","
            

    canvas.create_text(640,240,text="Checking for allergens...",font = "Helvetica 56 italic", fill = "#a79eff")
    canvas.create_text(640,340,text=allergyStr[:len(allergyStr)-1],font = "Helvetica 36 italic", fill = "#a79eff")
 
    
    canvas.create_rectangle(280,440,1010,600,fill = "white",width = 10,outline ='#a79eff')
    canvas.create_text(645,520,text = "Click to scan!", font = "Helvetica 46 bold italic")
    
def scannerMousePressed(event,data):
        mouseX = event.x
        mouseY = event.y
        if(mouseX>280 and mouseX<1010 and mouseY>440 and mouseY<600):
            barcodeScannerVideo.startBarcode()
            print("Found!", barcodeScannerVideo.found)
            
            

def scannerTimerFired(data):
    if(barcodeScannerVideo.found!=set()):
        data.foundBarcode = True
        for item in barcodeScannerVideo.found:
            data.barcode += str(item)
        data.curState = data.stateOptions[3]
        

        
        
##########################
# Barcode Check Mode #
##########################
def barcodeCheckRedrawAll(canvas,data):
    data.itemName = ""
    canvas.create_image(0,0, image=data.image3, anchor =NW)
    if(data.barcode in csvToDict.productDict):
        data.itemName = csvToDict.nameDict[data.barcode]+" - " +csvToDict.manuDict[data.barcode]
        canvas.create_text(640,240,text=data.itemName,font = "Helvetica 26 italic", fill = "#a79eff")
        canvas.create_text(640,300,text = "Is this correct?", font = "Helvetica 26 italic", fill = "#a79eff")
        #yes box
        canvas.create_rectangle(260,340,560,440,fill = "white", width = 5, outline= "#a79eff")
        canvas.create_text(410, 390, text = "Yes", font = "Helvetica 46 italic", fill = "black")
        #no box
        canvas.create_rectangle(700,340,1000,440,fill = "white", width = 5, outline = "#a79eff")
        canvas.create_text(850, 390, text = "No", font = "Helvetica 46 italic", fill = "black")
    elif(data.barcode[1:] in csvToDict.productDict):
        data.itemName = csvToDict.nameDict[data.barcode[1:]] +" - " + csvToDict.manuDict[data.barcode[1:]]
        canvas.create_text(640,240,text=data.itemName,font = "Helvetica 26 italic", fill = "#a79eff")
        canvas.create_text(640,300,text = "Is this correct?", font = "Helvetica 26 italic", fill = "#a79eff")
        #yes box
        canvas.create_rectangle(260,340,560,440,fill = "white", width = 5, outline= "#a79eff")
        canvas.create_text(410, 390, text = "Yes", font = "Helvetica 46 italic", fill = "black")
        #no box
        canvas.create_rectangle(700,340,1000,440,fill = "white", width = 5, outline = "#a79eff")
        canvas.create_text(850, 390, text = "No", font = "Helvetica 46 italic", fill = "black")
    elif("0" + data.barcode in csvToDict.productDict):
        data.itemName = csvToDict.nameDict["0" + data.barcode] + " - " + csvToDict.manuDict["0" + data.barcode]
        canvas.create_text(640,240,text=data.itemName,font = "Helvetica 18 italic", fill = "#a79eff")
        canvas.create_text(640,300,text = "Is this correct?", font = "Helvetica 26 italic", fill = "#a79eff")
        #yes box
        canvas.create_rectangle(260,340,560,440,fill = "white", width = 5, outline= "#a79eff")
        canvas.create_text(410, 390, text = "Yes", font = "Helvetica 46 italic", fill = "black")
        #no box
        canvas.create_rectangle(700,340,1000,440,fill = "white", width = 5, outline = "#a79eff")
        canvas.create_text(850, 390, text = "No", font = "Helvetica 46 italic", fill = "black")
    else:
        canvas.create_text(640,240,text="Product not found!",font = "Helvetica 46 italic", fill = "#a79eff")
        #### Need to Create box for implementing ur own!###
        
        canvas.create_text(640,390, text = "Input the products ingredients:", font = "Helvetica 46 italic", fill = "#a79eff")
        canvas.create_rectangle(10,440, 1270,500, fill = "white",width = 5, outline= "#a79eff")
        if(data.inputtingIngred==False):
            canvas.create_text(640,470,text = "Input Ingredients (comma seperated, 1 space after commas)", font = "Helvetica 26 italic")
        if(data.inputtingIngred==True):
            canvas.create_text(640,470, text = data.customIngred, font = "Helvetica 10 bold italic")
        canvas.create_rectangle (540,600,740,700,fill = "white", width = 5, outline = "#a79eff")
        canvas.create_text(640,650, text = "Submit!", font = "Helvetica 26 italic" )
            
        
    
def barcodeCheckKeyPressed(event,data):
    if(data.inputtingIngred==True):
        if(event.keysym=="BackSpace"):
            data.customIngred = data.customAllergen[:-1]
        elif(event.keysym=="space"):
            data.customIngred+=" "
        elif(event.keysym=="comma"):
            data.customIngred+=","
        else:
            data.customIngred += event.keysym
      
def barcodeCheckMousePressed(event,data):
    #canvas.create_rectangle(260,440, 1000,540, fill = "white",width = 5, outline= "#a79eff")
    if(event.x>10 and event.x<1270 and event.y>440 and event.y<500):
        data.inputtingIngred = True

    if(event.x>540 and event.x<740 and event.y>600 and event.y<700):
        data.inputtingIngred = False
        data.customIngredList = True
        data.ingList = data.customIngred.upper().split(",")
        print(data.ingList)
        if(allergyDetermine.isAllergic(data.selectedAllergies,data.ingList,data.optionalAllergens)):
            data.allerText = " "
            data.allerList = []
            data.allerList = allergyDetermine.returnAllergen(data.selectedAllergies,data.ingList,data.optionalAllergens)
            for item in data.allerList:
                data.allerText += (str(item) + ", ")
            data.curState = "unsafeFood"
        else: 
            data.curState = "safeFood"
    
    if(event.x>700 and event.x<1000 and event.y>340 and event.y<440):
        data.wrongCount +=1
        barcodeScannerVideo.found = set()
        data.barcode = ""
        data.customAllergen = ""
        print(barcodeScannerVideo.found)
        data.curState = "wrongItem"
        
    #This is super important and determines if the food is eatable!
    if(event.x>260 and event.x<560 and event.y>340 and event.y<440):
            print("yeehaw")
            data.ingList = []
            data.allerText = ""
            data.allerList = []
            if(data.barcode in csvToDict.productDict):
                print("barcode found! teehee")
               
                data.ingList = csvToDict.productDict[data.barcode].upper().split(',')
                
                
                if(allergyDetermine.isAllergic(data.selectedAllergies,data.ingList,data.optionalAllergens)):
                    data.allerList = []
                    data.allerList = allergyDetermine.returnAllergen(data.selectedAllergies,data.ingList,data.optionalAllergens)
                    for item in data.allerList:
                        data.allerText += (str(item) + ", ")
                    data.curState = "unsafeFood"
                else: 
                    data.curState = "safeFood"
                     
            #case to handle where first number is 0!
            elif(data.barcode[1:] in csvToDict.productDict):
                print("da barcode found! ")
                data.ingList = csvToDict.productDict[data.barcode[1:]].upper().split(',')
                print (data.ingList)
                print(allergyDetermine.isAllergic(data.selectedAllergies,data.ingList,data.optionalAllergens))
                if(allergyDetermine.isAllergic(data.selectedAllergies,data.ingList,data.optionalAllergens)):
                    data.allerList = []
                    data.allerList = allergyDetermine.returnAllergen(data.selectedAllergies,data.ingList, data.optionalAllergens)
                    for item in data.allerList:
                        data.allerText += (str(item) + ", ")
                    data.curState = "unsafeFood"
                else: 
                    data.curState = "safeFood"
            elif("0" + data.barcode in csvToDict.productDict):
                print("barcode found! ")
                data.ingList = csvToDict.productDict["0" + data.barcode].upper().split(',')
                print (data.ingList)
                print(allergyDetermine.isAllergic(data.selectedAllergies,data.ingList,data.optionalAllergens))
                if(allergyDetermine.isAllergic(data.selectedAllergies,data.ingList,data.optionalAllergens)):
                    data.allerList = []
                    data.allerList = allergyDetermine.returnAllergen(data.selectedAllergies,data.ingList, data.optionalAllergens)
                    for item in data.allerList:
                        data.allerText += (str(item) + ", ")
                    data.curState = "unsafeFood"
                else: 
                    data.curState = "safeFood"
            
                
####################################
# Wrong Item Scanned #
####################################
def wrongItemRedrawAll(canvas,data):
    canvas.create_image(0,0,image = data.rescanImage, anchor=NW)
    canvas.create_rectangle(380,440,900,540,fill="white",width = 5, outline = "#a79eff")
    canvas.create_text(640,490,text = "Click to scan again!", font = "Helvetica 46 italic", fill = "black" )
    
def wrongItemMousePressed(event,data):
    if(event.x>380 and event.x<900 and event.y>440 and event.y<540):
        barcodeScannerVideo.startBarcode()
        
def wrongItemTimerFired(data):
    if(barcodeScannerVideo.found!=set()):
        data.foundBarcode = True
        for item in barcodeScannerVideo.found:
            data.barcode += str(item)
        data.curState = data.stateOptions[3]

####################################
# Safe Food #
####################################
def safeFoodRedrawAll(canvas,data):
    canvas.create_image(0,0, image=data.safeImage, anchor =NW)
    canvas.create_rectangle(280,540 ,580,640, fill = "white", width =10, outline = "#a79eff")
    canvas.create_rectangle(700,540,1000,640,fill="white",width = 10, outline = "#a79eff")
    canvas.create_text(645,340,text = data.itemName + " is free of allergens!", font = "Helvetica 16 italic", fill = "#a79eff")
    canvas.create_text(430,590, text = "Scan Another",font = "Helvetica 26 italic", fill = "#a79eff")
    canvas.create_text(850,590, text = "Start Over",font = "Helvetica 26 italic", fill = "#a79eff")
    
def safeFoodMousePressed(event,data):
    if(event.x>280 and event.x<580 and event.y>540 and event.y<640):
        barcodeScannerVideo.found = set()
        data.barcode = ""
        #data.optionalAllergens = set()
        data.customAllergen = ""
        data.curState = "scanner"
        
    if(event.x>700 and event.x<1000 and event.y>540 and event.y<640):
        barcodeScannerVideo.found = set()
        data.barcode = ""
        data.customIngred = ""
        data.optionalAllergens = set()
        data.customAllergen = ""
        for item in data.allergyInput:
            item[1] = False
        data.curState = "home"
####################################
# UnSafe Food #
####################################
def unSafeFoodRedrawAll(canvas,data):
    canvas.create_image(0,0, image=data.unSafeImage, anchor =NW)
    canvas.create_text(645,340,text = "This product contains...", font = "Helvetica 56 italic", fill = "#a79eff")
    canvas.create_text(645,440,text = data.allerText[:-2], font = "Helvetica 16 italic", fill = "#a79eff")
    
    #need to make a scanner or go home. do scan another, or start over
    #scan another
    canvas.create_rectangle(530,540 ,730,640, fill = "white", width =10, outline = "#a79eff")
    #start over
    canvas.create_rectangle(830,540,1030,640,fill="white",width = 10, outline = "#a79eff")
    #Similar Products
    canvas.create_rectangle(230,540,430,640, fill = "white", width =10, outline = "#a79eff")
    
    canvas.create_text(630,590, text = "Scan Another",font = "Helvetica 26 italic", fill = "#a79eff")
    canvas.create_text(930,590, text = "Start Over",font = "Helvetica 26 italic", fill = "#a79eff")
    canvas.create_text(330,590, text = "Similar Products",font = "Helvetica 26 italic", fill = "#a79eff")
    
def unSafeFoodMousePressed(event,data):
    #scan another
    if(event.x>530 and event.x<730 and event.y>540 and event.y<640):
        barcodeScannerVideo.found = set()
        data.barcode = ""
       # data.optionalAllergens = set()
        data.customAllergen = ""
        data.curState = "scanner"
    #start over
    if(event.x>830 and event.x<1030 and event.y>540 and event.y<640):
        barcodeScannerVideo.found = set()
        data.barcode = ""
        data.optionalAllergens = set()
        data.customAllergen = ""
        data.customIngred = ""
        for item in data.allergyInput:
            item[1] = False
        data.curState = "home"
        
    
        
    #similar products 
    if(event.x>230 and event.x<430 and event.y>540 and event.y<640):
        print("simProdSelectAller", data.selectedAllergies)
        #set the data.reccommendProducts variable
        if(data.barcode in csvToDict.productDict):
            data.recommendProducts = reccommend.recommend2(data.barcode, data.selectedAllergies, data.optionalAllergens)  
        elif(data.barcode[1:] in csvToDict.productDict):
            data.recommendProducts = reccommend.recommend2(data.barcode[1:], data.selectedAllergies, data.optionalAllergens)
        elif("0" + data.barcode in csvToDict.productDict):
            data.recommendProducts = reccommend.recommend2("0" + data.barcode, data.selectedAllergies, data.optionalAllergens)
        elif(data.customIngredList == True):
            data.recommendProducts = reccommend.recommend3(data.ingList, data.selectedAllergies, data.optionalAllergens)
        
        print(data.recommendProducts)
        data.curState = "recommend"

            
        
        
####################################
# recommend #
####################################  
def recommendRedrawAll(canvas,data):
   
    if(data.recommendProducts!=[]):
        #need to make sure image is available!
        canvas.create_image(0,0, image=data.tryTheseImage, anchor =NW)
        
        #data.recommendedProducts is a list, need to keep track of index
        data.recImgLink = webscraping.getImage(data.recommendProducts[data.recProductsIndex])
        productName = data.recommendProducts[data.recProductsIndex]
        array = barcodeScannerVideo.url_to_image(data.recImgLink)
    
        
        data.recPhoto = ImageTk.PhotoImage(image = Image.fromarray(array))
        
    
        canvas.create_image(640,360,image = data.recPhoto )
        
        canvas.create_text(640,560, text = nameDict[productName], font = "Helvetica 26 bold italic", fill = "#a79eff")
        if(len(data.recommendProducts)>1):
            canvas.create_text(1180, 360, text = "Next", font = "Helvetica 46 bold italic", fill = "#a79eff")
        
            canvas.create_text(100, 360, text = "Prev", font = "Helvetica 46 bold italic", fill = "#a79eff")
    elif(data.recommendProducts == []):
        canvas.create_image(0,0, image=data.tryTheseImage, anchor =NW)
        canvas.create_text(640,360, text = "No recommended products found!", font = "Helvetica 46 bold italic" )
        
    canvas.create_rectangle(380,640 ,580,700, fill = "white", width =10, outline = "#a79eff")
    canvas.create_rectangle(700,640,900,700,fill="white",width = 10, outline = "#a79eff")
    canvas.create_text(480,670, text = "Scan Another",font = "Helvetica 26 italic", fill = "#a79eff")
    canvas.create_text(800,670, text = "Start Over",font = "Helvetica 26 italic", fill = "#a79eff")

   ## #create start over ###


def recommendMousePressed(event,data):
    if(data.recommendProducts!=[]):
        if(event.x>440 and event.x<840 and event.y>160 and event.y<560):
            link = webscraping.getStoreLink(data.recommendProducts[data.recProductsIndex])
            print("Opening link...")
            if(link!=None):
                webbrowser.open(str(link))
            

    if(event.x>1100 and event.x<1280 and event.y>260 and event.y<460):
        if(data.recommendProducts!=[]):
            if(data.recProductsIndex==len(data.recommendProducts)-1):
                data.recProductsIndex =  0
            else: 
                data.recProductsIndex +=1
                
    if(event.x>0 and event.x<200 and event.y>260 and event.y<460):
        if(data.recommendProducts!=[]):
            if(data.recProductsIndex==0):
                data.recProductsIndex = (len(data.recommendProducts))-1
            else: 
                data.recProductsIndex -=1
                
   
         
    if(event.x>380 and event.x<580 and event.y>640 and event.y<700):
        barcodeScannerVideo.found = set()
        data.barcode = ""
        #data.optionalAllergens = set()
        data.customAllergen = ""
        data.recProductsIndex = 0
        data.curState = "scanner"
        
    if(event.x>700 and event.x<900 and event.y>640 and event.y<700):
        barcodeScannerVideo.found = set()
        data.barcode = ""
        data.customIngred = ""
        data.optionalAllergens = set()
        data.customAllergen = ""
        data.recProductsIndex = 0
        for item in data.allergyInput:
            item[1] = False
        data.curState = "home"
        
        
####################
# Disclaimer Mode #
#####################
def disclaimerRedrawAll(canvas,data):
    canvas.create_image(0,0, image=data.disclaimerImage, anchor =NW)
    canvas.create_rectangle(540,600,740,700,fill = "white", width = 5, outline = "#a79eff")
    canvas.create_text(640, 650, text = "Home", font = "Helvetica 26 italic")
    
def disclaimerMousePressed(event,data):
    if(event.x>540 and event.x<740 and event.y>600 and event.y<700):
        data.curState = "home"

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280,720)