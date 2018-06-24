import sqlite3
import json
import requests
import os
from datetime import datetime as d
# import os.path
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "PupilPremiumTable.db")
if os.name == 'nt':
    logintext = "C:\\Users\\cervantes\\Downloads\\login.txt"
else:
    logintext = "/Users/eduardocervantes/Desktop/Macbook/login.txt"
# queries
daily_q = 'SELECT quote, dateSent, quoteID_FK, category FROM  dailyQview;'
insertQuoteH = 'INSERT INTO QuoteHistory VALUES (?, ?)'
sqlite_file = 'main/quotes_app.sqlite3'
insert_ehistory = '''INSERT INTO EHistory (dateSent, quoteID_FK, email_ID_FK)  SELECT  '1900-01-01' AS dateSent, q.quoteID_FK, e.ID
FROM  QuoteHistory q CROSS JOIN emailAddress e WHERE  (e.active = 1)  AND q.dateSent = date('now') 
AND q.quoteID_FK NOT IN (SELECT  quoteID_FK from EHistory WHERE dateSent='1900-01-01' OR dateSent > date('now', '-31 day'));'''
emailsQueue = '''SELECT firstName, emailAddress, emailID, quoteID_FK, quote FROM emailToSend ORDER BY RANDOM() LIMIT 5'''
updateHistoryQ = "UPDATE EHistory SET dateSent = ? WHERE email_ID_FK = ? and quoteID_FK =? "

# return random quote
def get_random_q():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row 
  c = conn.cursor()
  rows = c.execute('''select quote, ID from randomQview''').fetchall()
  conn.close()
  return json.dumps( [dict(ix) for ix in rows] )   

def insert_daily_q():
  currDate = d.now().strftime("%Y-%m-%d")
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row 
  c = conn.cursor()
  rows = c.execute('''select quote, ID from randomQview''').fetchall()
  for i in rows:
     c.execute(insertQuoteH, (currDate, i[1]))
     conn.commit()
  conn.close()   
  
def get_daily_q():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row 
  c = conn.cursor()
  rows = c.execute(daily_q).fetchall()
  conn.close()
  return json.dumps( [dict(ix) for ix in rows] )     

def send_quote(email, quote, fname, api_key ):
  # send via mailgun
  return requests.post(
        "https://api.mailgun.net/v3/mailgun.eddyizm.com/messages",
        auth=("api", api_key),
        data={"from": "quotes <postmaster@mg.eddyizm.com>",
              "to": email,
              "subject": "Hello {}".format(fname),
              "text": "Testing some Mailgun awesomness!"})

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
  conn.close()         

def get_api():
  with open(logintext, 'r') as g:
     login = g.read().splitlines()
     return login[0]
# process 5 emails at a time
def do_the_work():
  pass


#print(get_daily_q())
if __name__ == '__main__':
  print('in the main function!')  
  message = '''<html>
		<head>
		<title>Quotes.eddyizm.com</title>
		</head>
		<body>
		<p> {} </p>
		<table>
		<tr>
		<th></th>
		<th></th>
		</tr>
		<tr>
		<td><a href=\"http://quotes.eddyizm.com\">quotes</a> | <a href=\"https://play.google.com/store/apps/details?id=com.eddyizm.quotes\">new android app</a> |</td>
		<td><a href=http://quotes.eddyizm.com/unsubscribe.php?subscriptionId={}>unsubscribe</a></td>
		</tr>
		</table>
		</body>
		</html>'''.format('this is a quote - bob', 'test')
  #print (message)
  emails = get_email_queue()
  print (get_api())
  for e in emails:
    print (e[1])