# Loading the required libraries

# For automation and web scraping
import selenium  
from selenium import webdriver
# By will serve as a substitute for find_element_by_ method
from selenium.webdriver.common.by import By
# WebDriverWait and expected_conditions will delay the code execution until the required tag,link is loaded in the browser (useful for slow webpage)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# To delay the execution of the program
import time
import pandas as pd

# navigating driver to silver funds webpage

try:
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path = driver_path)
except:
    print("Something wrong with the driver path given for web browser")
    
try:
    # Opening the webpage
    driver.get('https://www.morningstar.in/default.aspx')
except:
    print("Webpage address not available")
    
try:
    # Clicking on Silver to get Silver Funds
    silver = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/form/div[4]/div[3]/div/div/div/div[2]/div/div[1]/div[4]/table/tbody/tr[1]/td[2]/a')))
    silver.click()
except:
    print("Link for silver funds not available.")

# extracting list of silver fund url's

try:
    # Extracting the element with all funds in the webpage
    all_funds_page = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_upnlReports"]/div[2]/div[1]/table/tbody/tr/td/table/tbody/tr[4]/td/div/table/tbody')))
except:
    print("Unable to find path to all silver funds element in the webpage.")

try:
    # making a list of all funds
    all_funds = all_funds_page.find_elements(By.TAG_NAME,'tr')

    fund_links_list = list()
    for fund in all_funds:
        fund_anchor_tags = fund.find_element(By.TAG_NAME,'a')
        fund_link = fund_anchor_tags.get_attribute('href')
        fund_links_list.append(fund_link)
    print("Successfully extracted silver fund url's.")
except:
    print("Unable to get a list of silver fund url's.")

# extracting fund name and code from each url

dict_list = list()

try:
    for link in fund_links_list:
        driver.get(link)

        try:
             # Extracting fund name and printing it
            fund_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="siteContent"]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div[1]/h2')))
        except: 
            print("Unable to extract fund name.")

        try:
            # Extracting fund code and printing it
            fund_code = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="siteContent"]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div[1]/span[1]')))
        except:
            print("unable to extract fund code.")

        dict_add = dict(Fund_Name = fund_name.text, Fund_Code = fund_code.text)
        dict_list.append(dict_add)

except:
    print("Something went wrong while extracting fund name and codes from url's.")
    
driver.quit()

# parsing data to pandas dataframe and saving in excel

try:
    df = pd.DataFrame(dict_list)
    df.to_excel('Silver_Funds.xlsx')
    print(df) # check the data frame
    print("Data Saved Successfully in variable df and excel file Silver_Funds.xlsx")
except:
    print("Unable to save data in dataframe.")
