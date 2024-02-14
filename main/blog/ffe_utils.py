import sqlite3
import requests
import os
from datetime import datetime as d

api_key = 'debug' # os.environ['MAILGUN_API']    

# queries
daily_q = 'SELECT quote, dateSent, quoteID_FK, category FROM  dailyQview;'
insertQuoteH = 'INSERT INTO QuoteHistory VALUES (?, ?)'
if os.name == 'nt':
  sqlite_file = 'main/quotes_app.sqlite3'
else:
  sqlite_file = "/home/eddyizm/sitefiles/eddyizm/main/quotes_app.sqlite3"

# flat file code
updateFFEVersion = "UPDATE FFEAppVersion SET DateUpdated = ?, Version = ?, URL = ? WHERE AppName = 'FlatFileExporter';"
getFFEVersion = "select Version, DateUpdated, URL from FFEAppVersion;"


def update_FFE(version: str, URL: str):
  ''' Update version available for app to check'''
  currDate = d.now().strftime("%Y-%m-%d")
  with sqlite3.connect(sqlite_file) as conn:
    c = conn.cursor()
    c.execute(updateFFEVersion, (currDate, version, URL))
    conn.commit()   
  

def get_FFE():
  ''' Get version and url '''
  with sqlite3.connect(sqlite_file) as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute(getFFEVersion).fetchall()
    data = {"Version": rows[0][0],
          "DateUpdated": rows[0][1],
          "URL": rows[0][2] }   
  return data


def get_daily_q(rtn_json):
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  rows = c.execute(daily_q).fetchall()
  conn.close()
  data = { "quote": rows[0][0],
    "dateSent": rows[0][1],
    "quoteID_FK": rows[0][2],
    "category": rows[0][3] 
  } 
  if rtn_json:
    return data
  else:
    return rows


def get_random_q():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  rows = c.execute('''select quote, ID from randomQview''').fetchall()
  data = { "quote": rows[0][0],
    "ID": rows[0][1]   
  } 
  conn.close()
  return data


def send_message(message):
  return requests.post(
        "https://api.mailgun.net/v3/mg.eddyizm.com/messages",
        auth=("api", api_key),
        data={"from": "Postmaster <postmaster@mg.eddyizm.com>",
              "to": 'eddyizm@gmail.com',
              "subject": "Website Inquiry",
              "text": message
              })
  