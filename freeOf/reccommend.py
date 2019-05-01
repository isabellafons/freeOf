######### This has 2 methods which are both used to recommend similar products #########
import allergyDetermine
import csvToDict
from csvToDict import productDict, nameDict, manuDict
import webscraping
import barcodeScannerVideo


###Make sure you check that rec products have a valid image###
def recommend3(unsafeIng, allergySet, optionalAllergenSet = set()):
    
    recFoods = []
    simIngredientCount = 0 
    for barcode in productDict:
        tmpIngList = productDict[barcode].split(",")
        
        
        for ing in tmpIngList:
            for ing2 in unsafeIng:
                if(ing in ing2) or (ing2 in ing):
                    simIngredientCount+=1
        
        if(len(recFoods)>5):
            break
        

        if(simIngredientCount>=len(unsafeIng)/1.5):
            if( allergyDetermine.isAllergic(allergySet,csvToDict.productDict[barcode].split(','),optionalAllergenSet)==False):
                if(csvToDict.productDict[barcode].split(',')[0]==unsafeIng[0]):
                    if(webscraping.getImage(barcode)!="assets/images/no-image-available.jpg"):
                        recFoods.append(barcode)

                        
        
        simIngredientCount = 0
        tmpIngList = []
        
    
    return recFoods


def recommend2(unsafeBar,allergySet,optionalAllergenSet = set()):
    
    recFoods = []
    tmpIngList  = []
    tmpNameList = []
   
    
    #name of unsafe barcode
    unsafeName = nameDict[unsafeBar]
    
    
    #need to parse the name into a list, last word needs to be same
    unsafeNameList = unsafeName.split(" ")
    print("unsafeName", unsafeNameList)
    
    
    #need list of unsafe products ingredients
    unsafeIng = productDict[unsafeBar].upper().split(",")
    print("unsafeING",unsafeIng)
    
    simNameCount = 0 
    simIngredientCount = 0 

    
    for barcode in productDict:
        tmpIngList = productDict[barcode].split(",")
        
        tmpNameList = nameDict[barcode].split(" ")
        foundNames = []
        tmpNameCount2 = 0 
        tmpIngCount2 = 0 
        
        if(len(recFoods)>10):
            break
    
        
        for name in tmpNameList:
            if name in unsafeNameList and name!="&" and name!="AND" and (name not in foundNames):
                simNameCount+=1
                foundNames.append(name)
        
        for ing in tmpIngList:
            
           # for ing2 in unsafeIng:
               # if(ing in ing2) or (ing2 in ing):
                if(ing.upper() in unsafeIng):
                    simIngredientCount+=1
        
        
        #case for where name is 1
        if(len(unsafeNameList)==1):
            if(unsafeName==nameDict[barcode]):
                if(simIngredientCount>=len(unsafeIng)/3):
                    if( allergyDetermine.isAllergic(allergySet,csvToDict.productDict[barcode].upper().split(','),optionalAllergenSet)==False):
                        try:
                            if(webscraping.getImage(barcode)!="assets/images/no-image-available.jpg"):
                               recFoods.append(barcode)
                        except:
                            continue
       
        else:
            if(simNameCount>1):
                if(simIngredientCount>=len(unsafeIng)/3):
                    if( allergyDetermine.isAllergic(allergySet,csvToDict.productDict[barcode].upper().split(','),optionalAllergenSet)==False):
                        try:
                            if(webscraping.getImage(barcode)!="assets/images/no-image-available.jpg"):
                               recFoods.append(barcode)
                               #print("temp ing added", productDict[barcode])
                        except:
                            continue
                            
     
                
                
        #add items with highest number of sim ingredients
        
       
        simNameCount = 0 
        simIngredientCount = 0
        tmpIngList = []
        tmpNameList = []
    print(recFoods)
    return recFoods
    
#print(recommend2("787692834617",{"Dairy"},{'chocolate'} ))
    



        
    
    
    