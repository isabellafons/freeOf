####The OpenCV file! this contains the barcode open CV scanner
#### as well as a method to get images from the web with open CV ####

###CITATION: BARCODE SCANNER IS ADAPTED FROM PYIMAGESEARCH.COM###
###https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-\
###scanner-with-zbar/###

# USAGE
# python barcode_scanner_video.py

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import urllib.request
from urllib.request import Request, urlopen






# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
found = set()

def url_to_image(url):
    
    headers ={'User-Agent': 'Mozilla/5.0'}
    
    req = Request(url = url, headers = headers)

    resp = urllib.request.urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype = "uint8")
    
    
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image3 = cv2.resize(image2,dsize=(300, 300), interpolation=cv2.INTER_CUBIC)
    
    
    
    
    
    return image3

def startBarcode():
    #found = set()
    barcode = None
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open(args["output"], "w")
    
    
    # loop over the frames from the video stream
    while (found==set()):
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
    
    # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
    
        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
    
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                print("new barcode found")
                print(barcodeData)
                csv.write("{},{}\n".format(datetime.datetime.now(),
                barcodeData))
                csv.flush()
                found.add(barcodeData)
                print("yee")
            
    
    # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # close the output CSV file do a bit of cleanup
    
    print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()
    print("done")
 