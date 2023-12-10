import webbrowser
import pyautogui
import pyperclip
import time
import re
import tkinter as tk
import os
import mysql.connector
from bs4 import BeautifulSoup


from win10toast import ToastNotifier
toast = ToastNotifier()

#less_than = "&?l?t?;?"
#number_or_decimal_dot = "[0-9.]+"
#number_or_decimal_comma= "[0-9,]+"
#normal_name_characters = "[a-zA-Z \&\-,.\/*]+"
#this = rf"Salt {less_than}"


#Redundant but kept
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

# Database functions - connection parameters and supporting code
db_config = {
    'host': '127.0.0.1',
    'user': 'PythonInsert',
    'password': 'Python123',
    'database': 'pvees'
}

def Check_Database_Status():
    try:
        connection = mysql.connector.connect(**db_config)
        DBStatusText.config(text="Available")
        window.after(1000,Check_Database_Status)
    except:
        DBStatusText.config(text="Not available")
        window.after(1000,Check_Database_Status)

def Failed_Link_Insert_Record(failed_link,error_info):
    # SQL statement to execute
    SQL_Statement = f"INSERT INTO `failedlinks`(`Link`, `ErrorInfo`) VALUES ('{failed_link}','{error_info}')"
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

        print(f"Row inserted.{failed_link}")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

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

# Supporting Functions for more regular mundane taks (non-database related)

def wait_for_download(filename_to_download):
    WAIT = 1
    directory_path = 'C:/Users/bohda/Documents/Python Codes/ProjectPVEES'
    while (WAIT):
        # List all files and directories in the specified path
        contents = os.listdir(directory_path)
        for item in contents:
            if item == filename_to_download:
                WAIT = 0
        time.sleep(0.5)
    #print("done!")
    
def Open_Webpage_and_Extract_All_HTML(URL):
    webbrowser.open(URL)
    time.sleep(4)

    pyautogui.moveTo(10, 200, duration=1)
    pyautogui.click()
    time.sleep(1)

    pyautogui.hotkey('ctrl','s')
    time.sleep(2)
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.5)

    HTML_File_Name = pyperclip.paste() + ".html"
    pyautogui.press('enter')
    wait_for_download(HTML_File_Name)
    pyautogui.hotkey('ctrl','w')
    time.sleep(1)

    # Specify the directory you want to list
    directory_path = 'C:/Users/bohda/Documents/Python Codes/ProjectPVEES'

    # List all files and directories in the specified path
    contents = os.listdir(directory_path)

    # Print the contents
    for item in contents:
        if HTML_File_Name == item:# broken but why
            #This means the file exists
            with open(item, 'r', encoding='utf-8') as file:
                HTML_contents = file.read()
            os.remove(item)
            return HTML_contents
    return None

def ResultsOfMultipleProductDataEntryPopUp(SuccessfulLinksNumber, PreExistingLinksNumber, FailedLinksNumber):
    ResultBox = tk.Toplevel(window)
    ResultBox.geometry("300x400")
    ResultBox.title("Results")
    SuccessfulLinksLabelItem = tk.Label(ResultBox,text="Successful links:")
    SuccessfulLinksLabelItem.grid(row=0,column=0)
    SuccessfulLinksLabelNumber = tk.Label(ResultBox,text=str(SuccessfulLinksNumber))
    SuccessfulLinksLabelNumber.grid(row=0,column=1)

    PreExistingLinksLabelItem = tk.Label(ResultBox,text="Already completed links:")
    PreExistingLinksLabelItem.grid(row=1,column=0)
    PreExistingLinksLabelNumber = tk.Label(ResultBox,text=str(PreExistingLinksNumber))
    PreExistingLinksLabelNumber.grid(row=1,column=1)

    FailedLinksLabelItem = tk.Label(ResultBox,text="Failed links:")
    FailedLinksLabelItem.grid(row=2,column=0)
    FailedLinksLabelNumber = tk.Label(ResultBox,text=str(FailedLinksNumber))
    FailedLinksLabelNumber.grid(row=2,column=1)

    ExitButton = tk.Button(ResultBox, text="Okay", command = ResultBox.destroy)
    ExitButton.grid(row=3,column=0, columnspan=2)

def StripErrorMessageOfQuotesAndReplaceWithSemiColons(error_to_deal_with):
    new_error_message = ""
    for character in error_to_deal_with:
        if character== "'":
            new_error_message += ";"
        else:
            new_error_message += character
    return new_error_message

def Escape_Quote_Mark_In_String(string_given):
    string_output = ""
    for each_character in string_given:
        if each_character == "'":
            string_output += ";" # Need to fix this
        else:
            string_output += each_character
    return string_output

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

def Extract_Pattern_Data_With_Range(content, pattern, start_extraction, end_extraction):
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

def NotifyMe(Successful, Failed, Pre_Existing,Total):
    toast.show_toast(
    "Project Protien Analysis",
    f"Successful: {Successful}/{Total} \n Failed: {Failed}/{Total} \n Pre-existing: {Pre_Existing}/{Total}",
    duration = 4,
    icon_path = "icon.ico",
    threaded = True,
    )

# Specific Data Extraction Algorithms

def ExtractName(URL_Content):
    soup = BeautifulSoup(URL_Content, 'html.parser')
    
    # Will edit this to use a database table instead that way I can add to it and edit this much easier.

    # Define your CSS selectors
    selectors = [
        # Website: https://www.dia.es/ 
        '#app > div > div > div > div.pdp-view__content > div.pdp-view__left-content > div.pdp-view__info > div.product-summary > h2',

        # Website: https://groceries.aldi.co.uk/
        '#vueProductDetails > div > div.col-lg-8 > div > div > h1',

        # Website: https://www.carrefour.es/
        '#app > div > main > div:nth-child(2) > div.product-header > h1',
        # Add more selectors as needed
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            print(element.get_text(strip=True))
            return element.get_text(strip=True)
    
    return "Not Available"

def ExtractPrice(URL_Content):
    pass

def ExtractTotalWeight(URL_Content):
    pass

def ExtractShop(URL_Content):
    pass

def ExtractCountry(URL_Content):
    pass

def ExtractCaloriesKCAL(URL_Content):
    pass

def ExtractFats(URL_Content):
    pass

def ExtractSats(URL_Content):
    pass

def ExtractCarbohydrates(URL_Content):
    pass

def ExtractSugars(URL_Content):
    pass

def ExtractFibre(URL_Content):
    pass

def ExtractProtien(URL_Content):
    pass

def ExtractSalt(URL_Content):
    pass

def TestFunctionForIndividualDataExtraction():
    LinkUsed = TestFunctionLinkEntry.get()
    URL_Content = Open_Webpage_and_Extract_All_HTML(LinkUsed)
    ExtractName(URL_Content)

# Single Link Data Extraction from Specific Websites
def PasteSingleProductLinkIntoEntry():
    LinkToPaste = pyperclip.paste()
    AddProductLinkEntry.delete(0, tk.END)
    AddProductLinkEntry.insert(0, LinkToPaste)

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
        ProductName = Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"primary_info":{"title":"[a-zA-Z0-9 ]+"},',15,-3)
    except:
        ProductName = Extract_Pattern_Data_With_Range(NutritionalElementValue,r'"">[A-Za-z0-9 -\'áéíóúüñÁÉÍÓÚÜÑ]+</',3,-2)
  
    ##### Price
    ProductPrice = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r',"price":[0-9]+.?[0-9]?[0-9]?,',9,-1))
    


    ##### Weight
    TotalWeight = Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"Contenido neto: [0-9]+.?[0-9]?[0-9]?[0-9]?K?g"',17,-2)
    if TotalWeight[-1:]=='K': #Weight in kg multiply by 1000
        TotalWeight = int(float(TotalWeight[:-1]) * 1000)
        print(TotalWeight)
    else:
        TotalWeight = int(TotalWeight)

    # Calories 
    Calories_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"nutritional_values":{"energy_value":[0-9]+,',37,-1))

    #### Fats
    Fats_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"title":"Grasas","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',25,-1))

    #### Sats
    SaturatedFats_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"de las cuales saturadas","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',34,-1))


    ##### Carbs
    Carbohydrates_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"Hidratos de Carbono","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',30,-1))


    #### Sugars
    Sugars_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"de los cuales azúcares","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',33,-1))

    # Fiber
    Fibers_per_100g = 0

    ### Protein
    Protein_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"Proteínas","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',20,-1))
    

    ## Salt
    try:
        Salt_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"Sal","value":[0-9]+.?[0-9]+?,',14,-1))
    except:
        Salt_per_100g = float(Extract_Pattern_Data_With_Range(NutritionalContentValues,r'"Sal","value":[0-9]+.?[0-9]?[0-9]?[0-9]?,',14,-1))

    
    ProtienValueDiaProduct, ProtienEnergyEfficiencyDiaProduct, ProteinValueEnergyEfficiencyDiaProduct = CalulateScores(Protein_per_100g,TotalWeight,ProductPrice,Calories_per_100g)
    return ProductName, ProductPrice,TotalWeight, Calories_per_100g, Fats_per_100g, SaturatedFats_per_100g, Carbohydrates_per_100g, Sugars_per_100g, Fibers_per_100g, Protein_per_100g, Salt_per_100g, ProtienValueDiaProduct, ProtienEnergyEfficiencyDiaProduct, ProteinValueEnergyEfficiencyDiaProduct, 0

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


    AldiUKProductName = Extract_Pattern_Data_With_Range(AllProductDataFromWebpage,r'<h1 class="my-0">[a-zA-Z0-9 \'\-\+&;\/%]+</h1>',17,-5) 
    AldiUKProductPrice = float(Extract_Pattern_Data_With_Range(AllProductDataFromWebpage,r'<span class="product-price h4 m-0 font-weight-bold">£[0-9].[0-9][0-9]</span>',53,-7))
    AldiProductTotalWeight = int(Extract_Pattern_Data_With_Range(AllProductDataFromWebpage,r'<td>[0-9]+g<[/]td>',4,-6))
    AldiNutritionalInformation = Extract_Pattern_Data_With_Range(AllProductDataFromWebpage,r'Energy [0-9]+kJ, [0-9]+kcal Fat &?l?t?;?[0-9]+.?[0-9]?[0-9]?g of which saturates &?l?t?;?[0-9]+.?[0-9]?[0-9]?g Carbohydrate &?l?t?;?[0-9]+.?[0-9]?[0-9]?g of which sugars &?l?t?;?[0-9]+.?[0-9]?[0-9]?g Fibre &?l?t?;?[0-9]+.?[0-9]?[0-9]?g Protein &?l?t?;?[0-9]+.?[0-9]?[0-9]?g Salt &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',0,200)
    #Needs much more filtering and protection

    print(AldiNutritionalInformation)


    AldiProductCalories = int(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'[0-9]+kcal',0,-4)) 
    AldiProductFats = float(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'Fat &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',4,-1)) 
    AldiProductSats = float(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'which saturates &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',16,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiProductCarbohydrates = float(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'Carbohydrate &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',13,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiProductSugars = float(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'which sugars &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',12,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiProductFibers = float(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'Fibre &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',6,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiProductProtien = float(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'Protein &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',8,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiProductSalt = float(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AldiNutritionalInformation,r'Salt &?l?t?;?[0-9]+.?[0-9]?[0-9]?g',5,-1),r'[0-9]+.?[0-9]?[0-9]?',0,20)) 
    AldiUKShop = "Aldi"
    AldiUKCountry = "United Kingdom"
    AldiUKProductPV, AldiUKProductPEE, AldiUKProductPVEES = CalulateScores(AldiProductProtien,AldiProductTotalWeight,AldiUKProductPrice,AldiProductCalories)
    InsertProductwithSQL(AldiUKCountry,"Manchester",Escape_Quote_Mark_In_String(AldiUKProductName),1,0,1,AldiUKShop,link,AldiUKProductPrice,AldiProductTotalWeight,AldiProductCalories,AldiProductFats,AldiProductSats,AldiProductCarbohydrates,AldiProductSugars,AldiProductFibers,AldiProductProtien,AldiProductSalt,AldiUKProductPV,AldiUKProductPEE,AldiUKProductPVEES,0 )

def Protected_Single_Item_Aldi_Code(URL_use):
    try:
        Extract_Data_From_ALDI_UK_Using_Inspect(URL_use)
        SingleProductLinkResultText.config(text="Success")
        return 1
    except Exception as error:
        SingleProductLinkResultText.config(text="Failed")
        Failed_Link_Insert_Record(URL_use,StripErrorMessageOfQuotesAndReplaceWithSemiColons(str(error)))
        return 0

def Extract_Single_Product_Data_From_Carrefour_Spain_Using_Save(link):
    page_data = Open_Webpage_and_Extract_All_HTML(link)
    Pattern_Price = r'<span class="buybox__price">\n[ ]+[0-9,]+[ ]€'
    Pattern_Name = r'<h1 class="product-header__name">\n.{1,}'
    Pattern_Weight = r'<span class="nutrition-more-info__list-value">\n[ ]+[0-9]+ g'
    Pattern_Fats = r'<span>Grasas \(g\)<\/span><\/span><span class="nutrition-legend__fright">&?l?t?;?[0-9]+.?[0-9]?[0-9]?[0-9]? g <\/span>'
    Pattern_Sats = r'de las cuales Saturadas \(g\)\n.{1,58}' # Need to search for the specific number
    Pattern_Carbohydrates = r'<p class="nutrition-legend__value"><span class="nutrition-legend__hydrates"><span class="nutrition-legend__color-box c2"><\/span><span>Hidratos de carbono \(g\)<\/span><\/span><span class="nutrition-legend__fright">[0-9.]+ g <\/span><\/p>'

def Extract_Data_From_BMUrban_Spain_Using_Inspect(link):
    pass

def Extract_Data_From_Tesco_UK_Using_Inspect(link):
    pass


# Multiple Products extracted from website functions
def PasteMultipleProductLinkIntoEntry():
    LinkToPaste = pyperclip.paste()
    MultipleProductLinkEntry.delete(0, tk.END)
    MultipleProductLinkEntry.insert(0, LinkToPaste)

def PasteTestFunctionLinkIntoEntry():
    LinkToPaste = pyperclip.paste()
    TestFunctionLinkEntry.delete(0, tk.END)
    TestFunctionLinkEntry.insert(0, LinkToPaste)

def Aldi_UK_Automated_Pull_In(link_to_page_1): # Works well but still uses inspect could be improved
    PATTERN_FOR_NUMBER_OF_PRODUCTS = r'<h1 class="font-weight-normal">[a-zA-Z ]+\(<span>[0-9]+<\/span>\)'
    PATTERN_FOR_PRODUCT_LINKS = r'href="/en-GB/[A-Za-z-0-9%\';&]+/[0-9]+"'
    PATTERN_FOR_NUMBER_OF_PAGES = r'&nbsp;of [0-9]+&nbsp'
    
    # Open URL in Chrome
    Link_To_Page_without_Number = Extract_Pattern_Data_With_Range(link_to_page_1,r'https://[a-zA-Z.\-/]+\?',0,200) + "&page="
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


    ## Now grab data on number of webpages to use:
    Number_of_Pages = int(Extract_Pattern_Data_With_Range(Extract_Pattern_Data_With_Range(AllProductsFromWebpage,PATTERN_FOR_NUMBER_OF_PAGES,0,100),r'[0-9]+',0,100))
    print(Number_of_Pages)

    pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on macOS

    Product_Links = []

    for page_number in range(1,Number_of_Pages+1):
        Page_Link = Link_To_Page_without_Number + str(page_number)
        webbrowser.open(Page_Link)

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

        AllProductsFromSpecificWebpage = pyperclip.paste()
        # Search for the pattern in the text
        Matches_Product_Links = re.findall(PATTERN_FOR_PRODUCT_LINKS, AllProductsFromSpecificWebpage)

        # Print all matches       
        for match in Matches_Product_Links:
            ADD = 1
            for PL in Product_Links:
                if PL == "https://groceries.aldi.co.uk" + match[6:-1]:
                    ADD=0
            if ADD == 1:
                Product_Links.append("https://groceries.aldi.co.uk" + match[6:-1])

        # Close the browser tab
        pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' on macOS
    print(Product_Links)
    TOTAL_PRODUCTS = len(Product_Links)
    SUCCESSFUL_LINKS = 0
    PREEXISTING_LINKS = 0
    FAILED_LINKS = 0
    for product_link in Product_Links:
        SuccessOnLink = Protected_Single_Item_Aldi_Code(product_link)
        if SuccessOnLink == 1:
            SUCCESSFUL_LINKS +=1
            NotifyMe(SUCCESSFUL_LINKS,FAILED_LINKS,PREEXISTING_LINKS,TOTAL_PRODUCTS)
        else:
            FAILED_LINKS += 1
            NotifyMe(SUCCESSFUL_LINKS,FAILED_LINKS,PREEXISTING_LINKS,TOTAL_PRODUCTS)
    ResultsOfMultipleProductDataEntryPopUp(SUCCESSFUL_LINKS,PREEXISTING_LINKS,FAILED_LINKS)




# Main code tie in
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
            except Exception as error:
                SingleProductLinkResultText.config(text="Failed")
                Failed_Link_Insert_Record(URL_use,StripErrorMessageOfQuotesAndReplaceWithSemiColons(str(error)))
        elif (URL_use[0:28]=="https://groceries.aldi.co.uk"):
            Protected_Single_Item_Aldi_Code(URL_use)
        else:
            print("This webpage URL is not covered yet. Sorry.")
    else:
        print("This product is already in the database.")

def MultipleResultsDataCode(results_page_link):
    if(Extract_Pattern_Data_With_Range(results_page_link,r'https://groceries.aldi.co.uk/en-GB/[a-zA-Z-/]+?',0,300)):
       #Aldi multiple items
       Aldi_UK_Automated_Pull_In(results_page_link)
    else:
        print("poop")

window = tk.Tk()
window.title("Extract PVEES Data From Webpage")
window.geometry("1920x1080")

DatabaseStatusText = tk.Label(window, text="Database: ")
DatabaseStatusText.grid(row=0,column=0)
DBStatusText = tk.Label(window, text="Checking")
DBStatusText.grid(row=0,column=1)

AddProductLinkText = tk.Label(window, text="Product Link: ")
AddProductLinkText.grid(row=1,column=0)
AddProductLinkEntry = tk.Entry(window)
AddProductLinkEntry.grid(row=1,column=1)
AddProductLinkPaste = tk.Button(window,text="Paste Link",command=PasteSingleProductLinkIntoEntry)
AddProductLinkPaste.grid(row=1,column=2)
AddProductLinkButton = tk.Button(window, text = "Add Link", command=SingleLinkDataCode)
AddProductLinkButton.grid(row=1,column=3)

SingleProductLinkResultText = tk.Label(window, text="Ready")
SingleProductLinkResultText.grid(row=2,column=0)


EmptyRow1 = tk.Label(window, text="     ")
EmptyRow1.grid(row=3,column=0)


MultipleProductLinkText = tk.Label(window, text="Results Page Link: ")
MultipleProductLinkText.grid(row=4,column=0)
MultipleProductLinkEntry = tk.Entry(window)
MultipleProductLinkEntry.grid(row=4,column=1)
MultipleProductLinkPaste = tk.Button(window,text="Paste Link",command=PasteMultipleProductLinkIntoEntry)
MultipleProductLinkPaste.grid(row=4,column=2)
MultipleProductLinkButton = tk.Button(window, text = "Add Link", command=lambda: MultipleResultsDataCode(MultipleProductLinkEntry.get()))
MultipleProductLinkButton.grid(row=4,column=3)

MultipleProductLinkResultText = tk.Label(window, text="Ready")
MultipleProductLinkResultText.grid(row=5,column=0)

ButtonExit = tk.Button(window, text="Exit program", command=window.destroy)
ButtonExit.grid(row=6,column=0)

TestFunctionLinkText = tk.Label(window, text="Test Function Link: ")
TestFunctionLinkText.grid(row=7,column=0)
TestFunctionLinkEntry = tk.Entry(window)
TestFunctionLinkEntry.grid(row=7,column=1)
TestFunctionLinkPaste = tk.Button(window,text="Paste Link",command=PasteTestFunctionLinkIntoEntry)
TestFunctionLinkPaste.grid(row=7,column=2)
TestFunctionLinkButton = tk.Button(window, text = "Add Link", command=TestFunctionForIndividualDataExtraction)
TestFunctionLinkButton.grid(row=7,column=3)



Check_Database_Status()
window.mainloop()