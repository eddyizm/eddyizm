import sqlite3
import json
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

insert_ehistory = '''INSERT INTO EHistory (dateSent, quoteID_FK, email_ID_FK)  SELECT  '1900-01-01' AS dateSent, q.quoteID_FK, e.ID
FROM  QuoteHistory q CROSS JOIN emailAddress e WHERE  (e.active = 1)  AND q.dateSent =  date('now')
AND q.quoteID_FK NOT IN (SELECT  quoteID_FK from EHistory WHERE dateSent='1900-01-01' OR dateSent > date('now', '-31 day'));'''
emailsQueue = '''SELECT firstName, emailAddress, emailID, quoteID_FK, quote FROM emailToSend ORDER BY RANDOM() LIMIT 5'''
updateHistoryQ = "UPDATE EHistory SET dateSent = ? WHERE email_ID_FK = ? and quoteID_FK =? "

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
  currDate = d.now().strftime("%Y-%m-%d")
  with sqlite3.connect(sqlite_file) as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute(getFFEVersion).fetchall()
    data = {"Version": rows[0][0],
          "DateUpdated": rows[0][1],
          "URL": rows[0][2] }   
  return data


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

def insert_daily_q():
  currDate = d.now().strftime("%Y-%m-%d")
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  rows = c.execute('''select quote, ID from randomQview''').fetchall()
  for i in rows:
     c.execute(insertQuoteH, (currDate, i[1]))
     conn.commit()
  c.execute(insert_ehistory)
  conn.commit()   
  conn.close()

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

def send_quote(email, quote, fname):
  return requests.post(
        "https://api.mailgun.net/v3/mg.eddyizm.com/messages",
        auth=("api", api_key),
        data={"from": "Postmaster <postmaster@mg.eddyizm.com>",
              "to": email,
              "subject": "Hello {}".format(fname),
              "text": quote,
              "html": '''<html>
                        <head>
                        <title>eddyizm.com/quotes</title>
                        </head>
                        <body>
                        <p> {} </p>
                        <table>
                        <tr>
                        <th></th>
                        <th></th>
                        </tr>
                        <tr>
                        <td><a href=\"https://eddyizm.com/quotes\">quotes</a> | <a href=\"https://play.google.com/store/apps/details?id=com.eddyizm.quotes\">android app</a> |</td>
                        <td><a href=http://quotes.eddyizm.com/unsubscribe.php?subscriptionId={}>unsubscribe</a></td>
                        </tr>
                        </table>
                        </body>
                        </html>'''.format(quote, 'test')})

# process 5 emails at a time
def get_email_queue():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  rows = c.execute(emailsQueue).fetchall()
  conn.close()
  if len(rows) > 0:
    return rows

def update_hist(date, emailID, quoteID):
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute(updateHistoryQ, (date, emailID, quoteID))
  conn.commit()
  conn.close()

def do_the_work():
  try:
    emails = get_email_queue()
    currDate = d.now().strftime("%Y-%m-%d")
    for e in emails:
      send_quote(e[1], e[4], e[0])
      update_hist(currDate, e[2], e[3])
      print ('email sent {}'.format(e[1]))
      
  except:
    pass

def send_message(message):
  return requests.post(
        "https://api.mailgun.net/v3/mg.eddyizm.com/messages",
        auth=("api", api_key),
        data={"from": "Postmaster <postmaster@mg.eddyizm.com>",
              "to": 'eddyizm@gmail.com',
              "subject": "Website Inquiry",
              "text": message
              })

if __name__ == '__main__':
  hour_check = d.utcnow().hour
  if hour_check == 12:
    insert_daily_q()
    print ('insert history block')
    
  if hour_check == 14 or hour_check == 16 or hour_check == 18 or hour_check == 20 or hour_check == 22:
    print ('in the work loop')
    # do_the_work()



  