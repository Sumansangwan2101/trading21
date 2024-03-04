# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:15:23 2024

@author: vikas
"""

from kiteconnect import KiteTicker, KiteConnect
import datetime
from datetime import date
import sys
import pandas as pd
import os

# import sqlite3
import login
 
cwd = os.chdir("D:\\Udemy\\Udemy python")
today = date.today().isoformat()
access_token_date = open("access_token_date.txt",'r').read()
if not today == access_token_date:
    login.autologin()

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
 
 
import mysql.connector
 
mysql_password = key_secret[5]
 
# MySQL database credentials
db_config = {
    'host': 'localhost',  # or your MySQL server IP
    'user': 'root',
    'password': "",
    'database': 'ZerodhaAlgo'
}
 
 
# Connect to the MySQL database
db = mysql.connector.connect(**db_config)
 
def create_tables(tokens):
    c = db.cursor()
    for i in tokens:
        c.execute("""
            CREATE TABLE IF NOT EXISTS TOKEN{} (
                ts DATETIME PRIMARY KEY,
                price DECIMAL(20, 5),
                volume BIGINT
            )
        """.format(i))
    db.commit()
 
 
def insert_ticks(ticks):
    c = db.cursor()
    for tick in ticks:
        try:
            tok = "TOKEN" + str(tick['instrument_token'])
            vals = [tick['exchange_timestamp'], tick['last_price'], tick['last_traded_quantity']]
            query = "INSERT INTO {} (ts, price, volume) VALUES (%s, %s, %s)".format(tok)
            c.execute(query, vals)
        except Exception as e:
            #print("insert data Error:", e)
            pass
    try:
        db.commit()
    except Exception as e:
        #print('******************************** ROLLBACK **************************')
        print("db committ Error:", e)
        db.rollback()
  
 
 
#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
 
def tokenLookup(instrument_df,symbol_list):
    """Looks up instrument token for a given script from instrument dump"""
    token_list = []
    for symbol in symbol_list:
        try:
            token_list.append(int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]))
        except:
            print('Ticker - {} not found in the instrument list of NSE'.format(symbol))            
    return token_list
 
 
tickersDf = pd.read_excel(D:\\Udemy\\Udemy python)
print(tickersDf.columns)
tickers = tickersDf['SYMBOL'].tolist()
 
#create KiteTicker object
kws = KiteTicker(key_secret[0],kite.access_token)
tokens = tokenLookup(instrument_df,tickers)
 
#create table
create_tables(tokens)
 
 
 
def on_ticks(ws,ticks):
    insert_tick=insert_ticks(ticks)        
    #print(ticks)
 
def on_connect(ws,response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL,tokens)
    
 
 
is_connected = False
 
while True:
    now = datetime.datetime.now()
    
    # Check if current time is between 9:15 AM and 15:30 PM
    if 9 <= now.hour < 15 or (now.hour == 9 and now.minute >= 15) or (now.hour == 15 and now.minute < 30):
        if not is_connected:
            kws.on_ticks = on_ticks
            kws.on_connect = on_connect
            kws.connect()
            is_connected = True
    elif now.hour >= 16 and now.minute >= 30:
        # Close the database connection and exit the program after 15:30
        db.close()
        sys.exit()