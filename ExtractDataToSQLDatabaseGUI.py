import webbrowser
import pyautogui
import pyperclip
import time
import re
import tkinter as tk

import mysql.connector

Screen_and_Inspect_Settings = {
    'screen_width' : 1920,
    'screen_height' : 1080,
    'Inspect_width' : 400,
    'Inspect_height' : 50
}

def TestSettingsCheck(link):
    # Open URL in Chrome
    webbrowser.open(link)

    # Wait for the page to load
    time.sleep(4)

    pyautogui.moveTo(10, 200, duration=1)
    pyautogui.click()

    #Wait 1 second
    time.sleep(1)

    # Right click
    pyautogui.click(button='right')

    #Wait 2 seconds
    time.sleep(1)

    # Go up 1 item to Inspect
    pyautogui.press('up')

    # Press Enter
    pyautogui.press('enter')

    time.sleep(1)

    
    #Move to 10, 100
    pyautogui.moveTo(1850, 140, duration=1)
    time.sleep(1)
    pyautogui.moveTo(1850, 140 + Screen_and_Inspect_Settings['Inspect_height'], duration=1)
    time.sleep(1)
    pyautogui.moveTo(1850 - Screen_and_Inspect_Settings['Inspect_width'], 140 + Screen_and_Inspect_Settings['Inspect_height'], duration=1)
    time.sleep(5)


    


# Database connection parameters
db_config = {
    'host': '127.0.0.1',
    'user': 'PythonInsert',
    'password': 'Python123',
    'database': 'pvees'
}

def Check_If_URL_Exists_In_Database(url):
    # Create a connection to the database
    connection = mysql.connector.connect(**db_config)

    try:
        # Create a cursor object
        cursor = connection.cursor()

        # SQL statement to execute
        SQLFindStatement = f"SELECT * FROM `products` WHERE Link = %s"

        # Execute the SQL statement
        cursor.execute(SQLFindStatement, (url,))

        # Fetch one record, if available
        record = cursor.fetchone()

        # Check if a record was found
        if record:
            #print("exists")
            return True
        else:
            #print("does not exist")
            return False

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def CopyElementDataToClipboard(downs):
    time.sleep(0.1)
    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=-0.5)
    time.sleep(0.5)
    pyautogui.click(button='right')
    time.sleep(0.1)
    for _ in range(0,downs):
        pyautogui.press('down')
        time.sleep(0.1)
    pyautogui.press('right')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)

def Extract_Nutitional_Item_Value(content, pattern, start_extraction, end_extraction):
        # Search for the pattern in the text
        matches_dia_item_value = re.findall(pattern, content)

        # Print all matches
        for match in matches_dia_item_value:
            print(match, match[start_extraction:end_extraction])
            item_value = match[start_extraction:end_extraction]
        return item_value

def extract_shop_and_country(url):
    # Regular expression to match the shop name and country code
    match = re.search(r"www\.([A-Za-z0-9\-]+)\.(es|co\.uk|com|cz)", url)
    if match:
        shop = match.group(1).capitalize()
        domain = match.group(2)
        # Map domain to country
        country_map = {'es': 'Spain', 'co.uk': 'United Kingdom', 'com': 'USA or International', 'cz': 'Czech Republic'}
        country = country_map.get(domain, 'Unknown')
        return shop, country
    return 'Unknown', 'Unknown'

def CalulateScores(Protein, TotalWeight, LocalCurrency, Calories):
    ProteinValue = Protein * TotalWeight / (LocalCurrency * 100)
    ProteinEnergyEfficiency = Protein / Calories
    ProteinValueEnergyEfficiency = ProteinEnergyEfficiency * ProteinValue
    return ProteinValue, ProteinEnergyEfficiency, ProteinValueEnergyEfficiency

def Open_and_Copy_Webpage_Contents(url):
    # Open URL in Chrome
    webbrowser.open(url)

    # Wait for the page to load
    time.sleep(5)

    # Move the mouse and click at position (10, 10)
    pyautogui.moveTo(10, 200, duration=1)
    pyautogui.click()

    # Select all and copy
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)  # Wait for selection
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)  # Wait for copy

    # Close the browser tab
    pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on macOS


    # Get the contents of the clipboard
    WebpageInfo = pyperclip.paste()

    print(WebpageInfo)
    return WebpageInfo

def InsertProductwithSQL(Country, City, Name, SnackBool, MealBool, IngredientBool, Shop, Link, LocalCurrency, TotalWeight, Calories, Fats, SatFats, Carbohydrates, Sugars, Fiber, Protein, Salt, ProteinValue, ProteinEnergyEfficiency, ProteinValueEnergyEfficiency, AccurateBool):
    # SQL statement to execute
    SQL_Statement = f"INSERT INTO `products`(`Country`, `City`, `Name`, `Snack`, `Meal`, `Ingredient`, `Shop`, `Link`, `LocalCurrency`, `TotalWeight`, `Calories`, `Fats`, `SaturatedFats`, `Carbohydrates`, `Sugars`, `Fiber`, `Protein`, `Salt`, `ProteinValue`, `ProteinEnergyEfficiency`, `ProteinValueEnergyEfficiency`, `Accurate`) VALUES ('{Country}','{City}','{Name}','{SnackBool}','{MealBool}','{IngredientBool}','{Shop}','{Link}','{LocalCurrency}','{TotalWeight}','{Calories}','{Fats}','{SatFats}','{Carbohydrates}','{Sugars}','{Fiber}','{Protein}','{Salt}','{ProteinValue}','{ProteinEnergyEfficiency}','{ProteinValueEnergyEfficiency}','{AccurateBool}')"
    print(SQL_Statement)

    try:
        # Establish a database connection
        connection = mysql.connector.connect(**db_config)

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the INSERT statement
        cursor.execute(SQL_Statement)

        # Commit the transaction
        connection.commit()

        print(f"Row inserted.{Name}")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def Extract_Data_From_Dia_Spain_Using_Inspect(link):

    # Open URL in Chrome
    webbrowser.open(link)

    # Wait for the page to load
    time.sleep(4)

    search_term_for_lots_of_information = "kcal" # Need the 2nd element where all the information is
    search_term_for_name = "product-title pdp-view__product-title"
    #Move to 10, 100
    pyautogui.moveTo(10, 200, duration=1)
    pyautogui.click()

    #Wait 1 second
    time.sleep(1)

    # Right click
    pyautogui.click(button='right')

    #Wait 2 seconds
    time.sleep(3)

    # Go up 1 item to Inspect
    pyautogui.press('up')

    # Press Enter
    pyautogui.press('enter')

    time.sleep(5)

    # Go to about 1800, 200
    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    pyautogui.click()

    # Then Ctrl + F [You will now be in the search box]
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(3)  # Wait for copy

    # Now paste the contents of the search tem you want likely lots of information
    pyautogui.typewrite(search_term_for_lots_of_information)

    time.sleep(3)

    pyautogui.press('enter')

    time.sleep(3)

    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    pyautogui.click()
    
    time.sleep(3)
    
    pyautogui.click(button='right')

    CopyElementDataToClipboard(6)
    
    # Get the contents of the clipboard
    NutritionalContentValues = pyperclip.paste()

    #Second time for name in case I need it
    pyautogui.moveTo(1850, 140, duration=1)
    for _ in range(250):
        pyautogui.click()
        time.sleep(0.01)  # Pause for 0.1 seconds between clicks

    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    pyautogui.click()

    # Then Ctrl + F [You will now be in the search box]
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)  # Wait for copy

    # Now paste the contents of the search tem you want likely lots of information
    pyautogui.typewrite(search_term_for_name)

    time.sleep(1)

    pyautogui.press('enter')

    CopyElementDataToClipboard(7)



    # Close the browser tab
    pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on macOS
 
    time.sleep(1)
    NutritionalElementValue = pyperclip.paste()
    time.sleep(1)

    try:
        ##### Name pain
        ProductName = Extract_Nutitional_Item_Value(NutritionalContentValues,r'"primary_info":{"title":"[a-zA-Z0-9 ]+"},',15,-3)
    except:
        ProductName = Extract_Nutitional_Item_Value(NutritionalElementValue,r'"">[A-Za-z0-9 -\'áéíóúüñÁÉÍÓÚÜÑ]+</',3,-2)
  
    ##### Price
    ProductPrice = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r',"price":[0-9]+.?[0-9]?[0-9]?,',9,-1))
    


    ##### Weight
    TotalWeight = Extract_Nutitional_Item_Value(NutritionalContentValues,r'"Contenido neto: [0-9]+.?[0-9]?[0-9]?[0-9]?K?g"',17,-2)
    if TotalWeight[-1:]=='K': #Weight in kg multiply by 1000
        TotalWeight = int(float(TotalWeight[:-1]) * 1000)
        print(TotalWeight)
    else:
        TotalWeight = int(TotalWeight)

    # Calories 
    Calories_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"nutritional_values":{"energy_value":[0-9]+,',37,-1))

    #### Fats
    Fats_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"title":"Grasas","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',25,-1))

    #### Sats
    SaturatedFats_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"de las cuales saturadas","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',34,-1))


    ##### Carbs
    Carbohydrates_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"Hidratos de Carbono","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',30,-1))


    #### Sugars
    Sugars_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"de los cuales azúcares","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',33,-1))

    # Fiber
    Fibers_per_100g = 0

    ### Protein
    Protein_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"Proteínas","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',20,-1))
    

    ## Salt
    try:
        Salt_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"Sal","value":[0-9]+.?[0-9]+?,',14,-1))
    except:
        Salt_per_100g = float(Extract_Nutitional_Item_Value(NutritionalContentValues,r'"Sal","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',14,-1))

    
    ProtienValueDiaProduct, ProtienEnergyEfficiencyDiaProduct, ProteinValueEnergyEfficiencyDiaProduct = CalulateScores(Protein_per_100g,TotalWeight,ProductPrice,Calories_per_100g)
    return ProductName, ProductPrice,TotalWeight, Calories_per_100g, Fats_per_100g, SaturatedFats_per_100g, Carbohydrates_per_100g, Sugars_per_100g, Fibers_per_100g, Protein_per_100g, Salt_per_100g, ProtienValueDiaProduct, ProtienEnergyEfficiencyDiaProduct, ProteinValueEnergyEfficiencyDiaProduct, 0

def Aldi_UK_Automated_Pull_In(link_to_page_1): # Needs work/barely started
    # Open URL in Chrome
    Link_To_Page_without_Number = Extract_Nutitional_Item_Value(link_to_page_1,r'https://[a-zA-Z.\-/]+\?',0,200) + "&page="
    webbrowser.open(link_to_page_1)

    # Wait for the page to load
    time.sleep(4)

    #Move to 10, 100
    pyautogui.moveTo(10, 200, duration=1)
    pyautogui.click()

    #Wait 1 second
    time.sleep(1)

    # Right click
    pyautogui.click(button='right')

    #Wait 2 seconds
    time.sleep(1)

    # Go up 1 item to Inspect
    pyautogui.press('up')

    # Press Enter
    pyautogui.press('enter')

    PATTERN_FOR_NUMBER_OF_PRODUCTS = r'<h1 class="font-weight-normal">[a-zA-Z ]+\(<span>[0-9]+<\/span>\)'
    PATTERN_FOR_PRODUCT_LINKS=r'href="/en-GB/[A-Za-z-0-9%\';&]+/[0-9]+"'

    time.sleep(1)

    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    pyautogui.click()

    # Then Ctrl + F [You will now be in the search box]
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)  # Wait for copy

    # Now paste the contents of the search tem you want likely lots of information
    pyautogui.typewrite("body")
    time.sleep(1)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    CopyElementDataToClipboard(6)

    time.sleep(1)


    AllProductsFromWebpage = pyperclip.paste()

    
    # Close the browser tab
    # pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on macOS



def Extract_Data_From_ALDI_UK_Using_Inspect(link):
    # Open URL in Chrome
    webbrowser.open(link)

    # Wait for the page to load
    time.sleep(4)

    #Move to 10, 100
    pyautogui.moveTo(10, 200, duration=1)
    pyautogui.click()

    #Wait 1 second
    time.sleep(1)

    # Right click
    pyautogui.click(button='right')

    #Wait 2 seconds
    time.sleep(1)

    # Go up 1 item to Inspect
    pyautogui.press('up')

    # Press Enter
    pyautogui.press('enter')

    time.sleep(1)

    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    pyautogui.click()

    # Then Ctrl + F [You will now be in the search box]
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)  # Wait for copy

    # Now paste the contents of the search tem you want likely lots of information
    pyautogui.typewrite("body")
    time.sleep(1)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.moveTo(1800, 140 + Screen_and_Inspect_Settings['Inspect_height'] - 5, duration=1)
    CopyElementDataToClipboard(6)

    time.sleep(1)


    AllProductDataFromWebpage = pyperclip.paste()
    
    # Close the browser tab
    pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on macOS


    AldiUKProductName = Extract_Nutitional_Item_Value(AllProductDataFromWebpage,r'<h1 class="my-0">[a-zA-Z0-9 \'\-\+&;\/%]+</h1>',17,-5) 
    AldiUKProductPrice = float(Extract_Nutitional_Item_Value(AllProductDataFromWebpage,r'<span class="product-price h4 m-0 font-weight-bold">£[0-9].[0-9][0-9]</span>',53,-7))
    AldiProductTotalWeight = int(Extract_Nutitional_Item_Value(AllProductDataFromWebpage,r'<td>[0-9]+g<[/]td>',4,-6))
    AldiNutritionalInformation = Extract_Nutitional_Item_Value(AllProductDataFromWebpage,r'Energy [0-9]+kJ, [0-9]+kcal Fat [0-9]+.?[0-9]?[0-9]?g of which saturates [0-9]+.?[0-9]?[0-9]?g Carbohydrate [0-9]+.?[0-9]?[0-9]?g of which sugars [0-9]+.?[0-9]?[0-9]?g Fibre [0-9]+.?[0-9]?[0-9]?g Protein [0-9]+.?[0-9]?[0-9]?g Salt &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',0,200)
    #Needs much more filtering and protection

    print(AldiNutritionalInformation)


    AldiProductCalories = int(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'[0-9]+kcal',0,-4)) 
    AldiProductFats = float(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'Fat [0-9]+.?[0-9]?[0-9]?g',4,-1)) 
    AldiProductSats = float(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'which saturates [0-9]+.?[0-9]?[0-9]?g',16,-1)) 
    AldiProductCarbohydrates = float(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'Carbohydrate [0-9]+.?[0-9]?[0-9]?g',13,-1)) 
    AldiProductSugars = float(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'which sugars [0-9]+.?[0-9]?[0-9]?g',13,-1)) 
    AldiProductFibers = float(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'Fibre [0-9]+.?[0-9]?[0-9]?g',6,-1)) 
    AldiProductProtien = float(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'Protein [0-9]+.?[0-9]?[0-9]?g',8,-1)) 
    AldiProductSalt = float(Extract_Nutitional_Item_Value(Extract_Nutitional_Item_Value(AldiNutritionalInformation,r'Salt &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',5,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiUKShop = "Aldi"
    AldiUKCountry = "United Kingdom"
    AldiUKProductPV, AldiUKProductPEE, AldiUKProductPVEES = CalulateScores(AldiProductProtien,AldiProductTotalWeight,AldiUKProductPrice,AldiProductCalories)
    InsertProductwithSQL(AldiUKCountry,"Manchester",AldiUKProductName,1,0,1,AldiUKShop,link,AldiUKProductPrice,AldiProductTotalWeight,AldiProductCalories,AldiProductFats,AldiProductSats,AldiProductCarbohydrates,AldiProductSugars,AldiProductFibers,AldiProductProtien,AldiProductSalt,AldiUKProductPV,AldiUKProductPEE,AldiUKProductPVEES,0 )







def Extract_Data_From_Carrefour_Spain_Using_Inspect(link):
    pass 

def Extract_Data_From_BMUrban_Spain_Using_Inspect(link):
    pass

def Extract_Data_From_Tesco_UK_Using_Inspect(link):
    pass











def extract_product_info(contents): #chatgpt
    # Define regular expressions for each piece of information
    item_name_regex = r"\b[A-Za-z]+[ A-Za-z]+\b"
    item_price_regex = r"(\d+,\d{2}|\d+.\d{2}) €"
    item_weight_regex = r"(\d+ g)"
    calories_regex = r"(\d+ Kcal)"
    fats_regex = r"Grasas \(g\)\n(\d+\.?\d*) g"
    sat_fats_regex = r"de las cuales Saturadas \(g\)\n(\d+\.?\d*) g"
    carbs_regex = r"Hidratos de carbono \(g\)\n(\d+\.?\d*) g"
    sugars_regex = r"de las cuales Azúcares \(g\)\n(\d+\.?\d*) g"
    fiber_regex = r"Fibra alimentaria \(g\)\n(\d+\.?\d*) g"
    protein_regex = r"Proteínas \(g\)\n(\d+\.?\d*) g"
    salt_regex = r"Sal \(g\)\n(\d+\.?\d*) g"

    # Search for each piece of information in the contents
    item_name = re.search(item_name_regex, contents)
    item_price = re.search(item_price_regex, contents)
    item_weight = re.search(item_weight_regex, contents)
    calories = re.search(calories_regex, contents)
    fats = re.search(fats_regex, contents)
    sat_fats = re.search(sat_fats_regex, contents)
    carbs = re.search(carbs_regex, contents)
    sugars = re.search(sugars_regex, contents)
    fiber = re.search(fiber_regex, contents)
    protein = re.search(protein_regex, contents)
    salt = re.search(salt_regex, contents)

    # Extract the information if found, else default to 0
    product_info = {
        "Item Name": item_name.group(0) if item_name else "0",
        "Item Price": item_price.group(1).replace(',', '.') if item_price else "0.00",
        "Item Weight (g)": int(item_weight.group(1).replace(' g', '')) if item_weight else 0,
        "Calories (per 100g)": int(calories.group(1).replace(' Kcal', '')) if calories else 0,
        "Fats (per 100g)": float(fats.group(1)) if fats else 0,
        "Saturated Fats (per 100g)": float(sat_fats.group(1)) if sat_fats else 0,
        "Carbohydrates (per 100g)": float(carbs.group(1)) if carbs else 0,
        "Sugars (per 100g)": float(sugars.group(1)) if sugars else 0,
        "Fiber (per 100g)": float(fiber.group(1)) if fiber else 0,
        "Protein (per 100g)": float(protein.group(1)) if protein else 0,
        "Salt (per 100g)": float(salt.group(1)) if salt else 0
    }

    return product_info



def Extract_Data(Link, contents):
    Shop, Country = extract_shop_and_country(Link)

    pattern_cost = r'([0-9]+),([0-9])([0-9]) €'
    matches_cost = re.findall(pattern_cost,contents)
    for match in matches_cost:
        print(match)
        options = []
        if(not (match[0] == '0' and match[1] == '0' and match[2] == '0')):
            options.append(match[0]+"."+ match[1] + match[2])
    CostLocalCurrency = options[0]
    
    print(Country, Shop, CostLocalCurrency)


def Extract_Data_Dia(contents,Link):
    # Regular expression pattern to find a number up to 10000 followed by 'kcal'
    Shop, Country = extract_shop_and_country(Link)

    pattern_cals = r'\b([1-9]\d{0,3}|10000)kcal\b'

    # Search for the pattern in the text
    matches_cals = re.findall(pattern_cals, contents)

    # Print all matches
    for match in matches_cals:
        print(match)
        CALORIES_PER_100G = match
    
    pattern_weight_g =  r'Contenido neto: ([1-9]\d{0,3}|10000)g'

    # Search for the pattern in the text
    matches_weight_g = re.findall(pattern_weight_g, contents)

    # Print all matches
    for match in matches_weight_g:
        print(match)
        TOTAL_WEIGHT = match
    
    pattern_weight_kg =  r'Contenido neto: ([1-9]\d{0,3}|10000)kg'

    # Search for the pattern in the text
    matches_weight_kg = re.findall(pattern_weight_kg, contents)

    # Print all matches
    for match in matches_weight_kg:
        print(match)
        match = str(int(match) * 1000)
        TOTAL_WEIGHT = match

    print(CALORIES_PER_100G, TOTAL_WEIGHT)

def PasteSingleProductLinkIntoEntry():
    LinkToPaste = pyperclip.paste()
    AddProductLinkEntry.delete(0, tk.END)
    AddProductLinkEntry.insert(0, LinkToPaste)

def SingleLinkDataCode(): # Main CODE
    URL_use =AddProductLinkEntry.get()
    #TestSettingsCheck(URL_use)
    #WP_info = Open_and_Copy_Webpage_Contents(URL_use)
    if(not Check_If_URL_Exists_In_Database(URL_use)):
        #We can try to grab the data and Insert into the database
        if(URL_use[0:19]=="https://www.dia.es/"):
            try:
                Shop_Dia, Country_Dia = extract_shop_and_country(URL_use)
                print(Shop_Dia, Country_Dia)
                DiaProductName, DiaProductPrice,DiaTotalWeight, DiaCalories_per_100g, DiaFats_per_100g, DiaSaturatedFats_per_100g, DiaCarbohydrates_per_100g, DiaSugars_per_100g, DiaFibers_per_100g, DiaProtein_per_100g, DiaSalt_per_100g, DiaProtienValueDiaProduct, DiaProtienEnergyEfficiencyDiaProduct, DiaProteinValueEnergyEfficiencyDiaProduct, Accurate = Extract_Data_From_Dia_Spain_Using_Inspect(URL_use)
                Snack, Ingredient, Meal = 1, 1, 0
                InsertProductwithSQL(Country_Dia,"Pamplona",DiaProductName,Snack,Meal,Ingredient,Shop_Dia,URL_use,DiaProductPrice,DiaTotalWeight,DiaCalories_per_100g,DiaFats_per_100g,DiaSaturatedFats_per_100g,DiaCarbohydrates_per_100g,DiaSugars_per_100g,DiaFibers_per_100g,DiaProtein_per_100g,DiaSalt_per_100g,DiaProtienValueDiaProduct,DiaProtienEnergyEfficiencyDiaProduct,DiaProteinValueEnergyEfficiencyDiaProduct,Accurate)
                SingleProductLinkResultText.config(text="Success")
            except:
                SingleProductLinkResultText.config(text="Failed")
        elif (URL_use[0:28]=="https://groceries.aldi.co.uk"):
            try:
                Extract_Data_From_ALDI_UK_Using_Inspect(URL_use)
                SingleProductLinkResultText.config(text="Success")
            except:
                SingleProductLinkResultText.config(text="Failed")
        else:
            print("This webpage URL is not covered yet. Sorry.")
    else:
        print("This product is already in the database.")


window = tk.Tk()
window.title("Extract PVEES Data From Webpage")
window.geometry("1920x1080")

AddProductLinkText = tk.Label(window, text="Product Link: ")
AddProductLinkText.grid(row=0,column=0)
AddProductLinkEntry = tk.Entry(window)
AddProductLinkEntry.grid(row=0,column=1)
AddProductLinkPaste = tk.Button(window,text="Paste Link",command=PasteSingleProductLinkIntoEntry)
AddProductLinkPaste.grid(row=0,column=2)
AddProductLinkButton = tk.Button(window, text = "Add Link", command=SingleLinkDataCode)
AddProductLinkButton.grid(row=0,column=3)

SingleProductLinkResultText = tk.Label(window, text="Ready")
SingleProductLinkResultText.grid(row=1,column=0)


ButtonExit = tk.Button(window, text="Exit program", command=window.destroy)
ButtonExit.grid(row=3,column=0)

window.mainloop()