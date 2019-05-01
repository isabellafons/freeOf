###This file has two main functions, one to determine if you are allergic to something
#### and one to return the specific ingredients you are allergic too ###

allergyDictionary = dict()

allergyDictionary["Dairy"] = {"BUTTER FAT","BUTTER OIL","BUTTER ACID",
"BUTTER ESTER","BUTTERMILK","CASEIN","CASEIN HYDROLYSATE","CASEINATES","CHEESE",
"COTTAGE CHEESE","CREAM","CURDS","CUSTARD","DIACETYL","GHEE","HALF-AND-HALF",
"LACTALBUMIN","LACTALBUMIN PHOSPHATE","LACTOFERRIN","LACTOSE","LACTULOSE","MILK",
"CONDENSED MILK","MILK DERIVATIVE","DRY MILK","EVAPORATED MILK","GOAT'S MILK",
"LOWFAT MILK","MALTED MILK","MILKFAT","NONFAT MILK","POWDERED MILK","MILK PROTEIN"
"SKIMMED MILK","MILK SOLIDS","WHOLE MILK","MILK PROTIEN HYDOLYSATE","PUDDING",
"RECALDENT","RENNET CASEIN","SOUR CREAM","SOUR CREAM SOLIDS","SOUR MILK SOLIDS",
"TAGATOSE","WHEY","WHEY PROTEIN","WHEY PROTEIN HYDROLYSATE","YOGURT","CREAM"}

allergyDictionary["Gluten"] = {"BREAD CRUMBS","BULGUR","CEREAL EXTRACT","CLUB WHEAT",
"COUSCOUS","CRACKER MEAL","DURUM","EINKORN","EMMER","FARINA","FARRO","FLOUR","ALL PURPOSE FLOUR",
"BREAD FLOUR","CAKE FLOUR","DURUM FLOUR","ENRICHED FLOUR","GRAHAM FLOUR","HIGH GLUTEN FLOUR",
"HIGH PROTEIN FLOUR","INSTANT FLOUR","PASTRY FLOUR","SELF-RISING FLOUR","SOFT WHEAR FLOUR",
"STEEL GROUND FLOUR","STONE GROUND FLOUR","WHOLE WHEAT FLOUR","FREEKAH","HYRDOLYZED WHEAT PROTEIN",
"KAMUT","MATZOH","MATZOH MEAL","MATZO","MATZAH","MATZA","PASTA","SEITAN","SEMOLINA","SPELT",
"SPROUTED WHEAT","TRITICALE","VITAL WHEAT GLUTEN","WHEAT BRAN","BRAN WHEAT","DURUM WHEAT",
"GERM WHEAT","WHEAT GLUTEN","GRASS WHEAT","WHEAT MALT","WHEAT SPROUTS","WHEAT STARCH",
"WHEAT BRAN HYDROLYSATE","WHEAT GERM OIL","WHEAT GRASS","WHEAT PROTEIN ISOLATE",
"WHOLE WHEAT BERRIES", "WHEAT", "WHOLE GRAIN WHEAT"}

allergyDictionary["Eggs"] = {"ALBUMIN","ALBUMEN","EGG","DRIED EGG","POWDERED EGG",
"EGG SOLIDS","EGG WHITE","EGG WHITES","EGG YOLK","EGG YOLKS","EGGNOG","GLOBULIN",
"LIVETIN","LYSOZYME","MAYONAISE","MERINGUE","MERINGUE POWDER",
"SURIMI","VITELLIN","OVALBUMIN"}

allergyDictionary['Soy'] = {"EDAMAME","MISO","NATTO","SOY","SOY ALBUMIN","SOY CHEESE", "SOY FIBER","SOY FLOUR","SOY GRITS","SOY ICE CREAM","SOY MILK","SOY NUTS",
"SOY SPROUTS","SOY YOGURT","SOYA","SOYBEAN","SOY CURD","SOY GRANULES","SOY PROTEIN",
"SOY PROTEIN CONCENTRATE","HYDROLYZED SOY PROTEIN","SOY PROTEIN ISOLATE","SHOYU",
"SOY SAUCE","TAMARI","TEMPEH","TEXTURED VEGETABLE PROTEIN","TOFU","TVP"}

allergyDictionary["Shellfish"] = {"BARNACLE","CRAB","CRAWFISH","CRAWDAD","CRAYFISH",
"ECREVISSE","KRILL","LOBSTER","LANGOUSTE","LANGOUSTINE","MORETON","BAY BUGS","SCAMPI", "TOMALLEY","PRAWNS","SHRIMP","CREVETTE","SCAMPI"}

allergyDictionary["Tree Nuts"] = {"ALMOND","ALMONDMILK","ARTIFICIAL NUTS","BEECHNUT","BRAZIL NUT", "BUTTERNUT","CASHEW","CHESTNUT","CHINQUAPIN NUT","FILBERT","HAZELNUT","GIANDUJA",
"GINKGO NUT","HICKORY NUT","LYCHEE","MACADAMIA NUT","MARZIPAN","ALMOND PASTE",
"NATURAL NUT EXTRACT","NUT BUTTERS","CASHEW BUTTER","ALMOND BUTTER","NUT MEAL",
"NUT MEAT","NUT PASTE","NUT PIECES","PECAN","PESTO","PILI NUT","PINE NUT",
"PISTACHIO","PRALINE","SHEA NUT","WALNUT", "BLACK WALNUT HULL EXTRACT","NATURAL NUT EXTRACT","WALNUT OIL","ALMOND OIL","WALNUT HULL EXTRACT"}

allergyDictionary["Peanuts"] = {"ARTIFICAL NUTS","BEER NUTS","PEANUT OIL","COLD PRESSED PEANUT OIL","EXPELLER PRESSED PEANUT OIL","EXTRUDED PEANUT OIL","GOOBERS","GROUND NUTS","MIXED NUTS","MONKEY NUTS","NUT MEAT","PEANUT BUTTER","PEANUT FLOUR","PEANUT PROTEIN HYDROLYSATE", "PEANUTS", "PEANUT", "PEANUT BUTTER"}

allergyDictionary["Sesame"] = {"BENNE","BENNE SEED","BENNISEED","GINGELL","GINGELLY OIL","HALVAH","SESAME FLOUR","SESAME OIL","SESAME PASTE","SESAME SALT","SESAME SEED","SESAMOL","SESAMUM INDICUM","SESEMOLINA","SIM SIM","TAHINI","TAHINA","TEHINA","TIL"}

#will need an allergen set, and a list of ingredients
#data.selectedAllergies is the allergy set, need to make ingredients into a list
def isAllergic(allergySet,ingredients,optionalAllergenSet = set()):
    for allergen in allergySet:
        if(len(ingredients)==1):
            for allergen in allergyDictionary[allergen]:
                if allergen in str(ingredients) and allergen!="BUTTER": return True
        else:
            for ingredient in ingredients:
                if(ingredient in allergyDictionary[allergen]) and ingredient!="BUTTER":
                    return True
                else:
                    for item in allergyDictionary[allergen]:
                        if item in ingredient and item!='BUTTER':
                            return True
    if(optionalAllergenSet!=set()):
        
        for optionAllergen in optionalAllergenSet:
            if(len(ingredients)==1):
                    if optionAllergen.upper() in str(ingredients): return True
            else:
                for ingredient in ingredients:
                    if(optionAllergen.upper() in ingredient):
                        return True
                    
                
    return False
    
def returnAllergen(allergySet,ingredients,optionalAllergenSet = set()):
    allergenList = []
    
    for allergen in allergySet:
        if(len(ingredients)==1):
            for allergen in allergyDictionary[allergen]:
                if allergen in str(ingredients):
                    if(allergen not in allergenList): 
                        allergenList.append(allergen)
        else:
            for ingredient in ingredients:
                if(ingredient in allergyDictionary[allergen]):
                    if(ingredient not in allergenList):
                        allergenList.append(ingredient)
                else:
                    for item in allergyDictionary[allergen]:
                        if item in ingredient:
                            if(item not in allergenList):
                                allergenList.append(item)
    if(optionalAllergenSet != set()):
        for optionalAllergen in optionalAllergenSet:
            if(len(ingredients)==1):
                    if optionalAllergen.upper() in str(ingredients): 
                        if(optionalAllergen not in allergenList):
                            allergenList.append(optionalAllergen)
            else:
                for ingredient in ingredients:
                    if(optionalAllergen.upper() in ingredient):
                        if(ingredient not in allergenList):
                            allergenList.append(ingredient)
                
                
    return allergenList