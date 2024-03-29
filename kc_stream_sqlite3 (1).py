# -*- coding: utf-8 -*-
"""
Zerodha Kite Connect - Storing tick level data in db

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from kiteconnect import KiteTicker, KiteConnect
import datetime
from datetime import date
import sys
import pandas as pd
import os
import sqlite3
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

db = sqlite3.connect('./ticks.db')

def create_tables(tokens):
    c=db.cursor()
    for i in tokens:
        c.execute("CREATE TABLE IF NOT EXISTS TOKEN{} (ts datetime primary key,price real(15,5), volume integer)".format(i))
    try:
        db.commit()
    except:
        db.rollback()

def insert_ticks(ticks):
    c=db.cursor()
    for tick in ticks:
        try:
            tok = "TOKEN"+str(tick['instrument_token'])
            vals = [tick['exchange_timestamp'],tick['last_price'], tick['last_traded_quantity']]
            query = "INSERT INTO {}(ts,price,volume) VALUES (?,?,?)".format(tok)
            c.execute(query,vals)
        except:
            pass
    try:
        db.commit()
    except:
        db.rollback()    


#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

def tokenLookup(instrument_df,symbol_list):
    """Looks up instrument token for a given script from instrument dump"""
    token_list = []
    for symbol in symbol_list:
        token_list.append(int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]))
    return token_list

#####################update ticker list######################################
tickers = ["NIFTY 50","NIFTY BANK"]
#############################################################################

#create KiteTicker object
kws = KiteTicker(key_secret[0],kite.access_token)
tokens = tokenLookup(instrument_df,tickers)

#create table
create_tables(tokens)


def on_ticks(ws,ticks):
    insert_tick=insert_ticks(ticks)
    print(ticks)

def on_connect(ws,response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL,tokens)
    

while True:
    now = datetime.datetime.now()
    if (now.hour >= 9 and now.minute >= 15 ):
        kws.on_ticks=on_ticks
        kws.on_connect=on_connect
        kws.connect()
    if (now.hour >= 15 and now.minute >= 30):
        sys.exit()

db.close()

"""
c.execute('SELECT name from sqlite_master where type= "table"')
c.fetchall()

c.execute('''PRAGMA table_info(TOKEN256265)''')
c.fetchall()

for m in c.execute('''SELECT * FROM TOKEN256265'''):
    print(m)
"""