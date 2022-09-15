# importing required libraries

# For automation and web scraping
import selenium  
# for saving the file and using hotkeys
import pyautogui 
from selenium import webdriver
# By will serve as a substitute for find_element_by_ method
from selenium.webdriver.common.by import By
# WebDriverWait and expected_conditions will delay the code execution until the required tag,link is loaded in the browser (useful for slow webpage)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# To delay the execution of the program
import time
import pandas as pd
# To open url
from urllib.request import urlopen
# To handle json files
import json

# scraping data from webpage

try:
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path = driver_path)
except:
    print("Something wrong with the driver path given for web browser")
    
# getting the link 
try:
    # Opening the webpage
    driver.get('https://www.amfiindia.com/nav-history-download')
except:
    print("Webpage address not available")
    
# Searching for the link to download nav report in text format

try:    
    nav_report = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'navhistorydownload')))
except:
    print("Either the webpage took too long to respond or the id for required element has changed")
    
# Clicking on the href link to navigate the driver to the webpage containing nav report    
try:
    nav_text_webpage = nav_report.find_element(By.TAG_NAME,'a')
    nav_text_webpage.click()
    time.sleep(2)
except:
    print("Link to navigate to NAV text report unavailable")

# Saving the file with desired file name (By default file is saved in downlods folder in C drive)
try:
    pyautogui.hotkey('ctrl','s')
    time.sleep(2)
    pyautogui.write('scraped_nav') 
    pyautogui.press('enter')
    print('File saved successfully.')
except:
    print('Something went wrong while saving the file')
    
time.sleep(2)
driver.quit()

# Parsing the text file to csv

try: 
    text_path = open(r"C:\Users\mksmu\Downloads\scraped_nav.txt")
except:
    print("Couldn't locate the downloaded text file")

def texttocsv(text_path):
    try:
        read_file = pd.read_csv (text_path)
        read_file.to_csv ('test.csv',index=None)  
        global df
        df = pd.read_csv('test.csv',delimiter = ';')
    except:
        print("Failed to parse text to csv.")
        
    try:
        df.dropna(inplace = True)
        df['ISIN Div Reinvestment'].replace('-',None,inplace = True)
        df.replace('^\s+', '', regex=True, inplace = True) #front
        df.replace('\s+$', '', regex=True, inplace = True) #end
        print("Dataframe containing all silver fund names, numbers and scheme codes created successfully.(Saved in variable 'df')")
    except:
        print('Failed to implement mehods on the dataframe.')    
    
texttocsv(text_path)


# Modifying the dataframe to extract url

try:
    nav_name = df.copy()
    nav_name['url'] = "https://api.mfapi.in/mf/" + nav_name['Scheme Code']
    nav_name.drop(columns = ['Scheme Code','Net Asset Value','Date','ISIN Div Payout/ ISIN Growth','ISIN Div Reinvestment'], inplace = True)
    print("Dataframe with Scheme name and url extracted successfully.(Saved in variable 'nav_name')")
except:
    print("Error in modifying the dataframe fields to get a list of url.")

# Extracting data from all url and saving in a dataframe

try:
    url_list = nav_name['url'].values
except:
    print("Failed to create a list of url to run.")
    
nav_values = pd.DataFrame()
    
# Only working with top 30 records as loading all takes a long time
for url in url_list[:30]:   
    
    try:    
        # Extracting data from url to dataframe
        response = urlopen(url)
        data_json = json.loads(response.read())
        date_nav = data_json['data']
        date_nav = pd.DataFrame.from_dict(date_nav)
    except:
        print("Failed to load data from url's to a dataframe.")
        
    try:
        # Modifying the dataframe as per our requirement
        date_nav.sort_values(by='date', inplace=True)
        date_nav.reset_index(inplace=True)
        date_nav.drop(columns=['index','date'], inplace=True)
        date_nav_add = date_nav.transpose()
        date_nav_add['url'] = url
        date_nav_add.set_index('url',inplace = True)
        nav_values = pd.concat([nav_values,date_nav_add])
    except:
        print("Failed to modify nav values dataframe as per requirement.")

# Merging the 2 dataframes with fund name and values

try:
    # Merging the 2 dataframes on basis of common index as url
    nav_name.set_index('url',inplace = True)
    nav_data = pd.concat([nav_values,nav_name[:30]],axis = 1)
    nav_data.set_index('Scheme Name', inplace = True)
    print("Successfully saved fund names and nav values in excel file 'Mutual_Funds.xlsx'.")   
except:
    print("Failed to merge the 2 dataframes with fund names and nav values.")

nav_data.to_excel('Mutual_Funds.xlsx')