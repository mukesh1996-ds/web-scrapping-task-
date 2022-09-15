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
'''
# Stage 1
def get_driver_path(path):
    
    In this stage we are going to get the driver path. 
    
    try:
        driver_path = path
        driver = webdriver.Chrome(executable_path = driver_path)
    except:
        print("Something wrong with the driver path given for web browser")

driver = get_driver_path('chromedriver.exe') # Executable file

# Stage 2 getting the link 
def url_link(path):
    try:
        # Opening the webpage
        driver.get(path)
    except:
        print("Webpage address not available")

url_link('https://www.amfiindia.com/nav-history-download')

'''
# Testing stage

def test_url_click(path = 'chromedriver.exe', url='https://www.amfiindia.com/nav-history-download'):
    try:
        driver_path = path
        driver = webdriver.Chrome(executable_path = driver_path)
    except:
        print("Something wrong with the driver path given for web browser")
    
    try:
        # Opening the webpage
        driver.get(url)
    except:
        print("Webpage address not available")


test_url_click()






    
