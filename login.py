# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:50:44 2024

@author: vikas
"""

from kiteconnect import KiteConnect
# from kiteconnect import KiteTicker
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import date
import os
from pyotp import TOTP


cwd = os.chdir("D:\\Udemy\\Udemy Python")

def autologin():
    token_path = "api_key.txt"
    # access_token = "access_token.txt"
    key_secret = open(token_path,'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    # service = webdriver.chrome.service.Service('./chromedriver')
    # service.start()
    # chrome_options = Options()
    # chrome_options.add_argument("--window-size=250,550")
    driver = webdriver.Chrome()
    driver.get(kite.login_url())
    print(kite.login_url())
    driver.implicitly_wait(5)
    username = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    password = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
    username.send_keys(key_secret[2])
    password.send_keys(key_secret[3])
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
    totp = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input')
    totp_token = TOTP(key_secret[4])
    token = totp_token.now()
    totp.send_keys(token)
    # driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[2]/button').click()
    time.sleep(10)
    request_token=driver.current_url.split('request_token=')[1][:32]
    print('request token is -:',request_token)
    data = kite.generate_session(request_token, api_secret=key_secret[1])
    print('access token is -:',data["access_token"])


    with open("access_token.txt", 'w') as file:
            file.write(data["access_token"])
    with open("access_token_date.txt", 'w') as file:
            file.write(date.today().isoformat())
    driver.quit()


# autologin()
# # Initialize Kite Connect with your API credentials
# request_token = open("request_token_file.txt",'r').read()
# key_secret = open("api_key.txt",'r').read().split()
# kite = KiteConnect(api_key=key_secret[0])
# data = kite.generate_session(request_token, api_secret=key_secret[1])
# with open('access_token.txt', 'w') as file:
#         file.write(data["access_token"])
