##### This file turns the CSVs from the USDA into dictionaries. ########

import csv

productDict = dict()
productSet = set()
nameDict = dict()
manuDict = dict()


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


    
#### CODE ADAPTED FROM https://stackoverflow.com/questions/8685809/writing-a-dictionary-to-a-csv-file-with-one-line-for-every-key-value ####
product_file = csv.DictReader(open("Products.csv"))

for row in product_file:
    barcode = (row["gtin_upc"])
    ingredients = (row["ingredients_english"])
    name = (row["long_name"])
    manufacturer = (row["manufacturer"])
    productDict[barcode] = ingredients
    nameDict[barcode] = name
    manuDict[barcode]  = manufacturer

    


    
