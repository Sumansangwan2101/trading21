# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:50:15 2024

@author: vikas
"""
from selenium import webdriver

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Open a website
# driver.get("https://www.example.com")

# Now you can interact with the webpage using the 'driver' object
# For example, you can find elements, click buttons, or extract information


driver.get("https://kite.zerodha.com/connect/login?api_key=wxo1l6ufwoypjwyc&v=3")

# Close the browser window when done
driver.quit()