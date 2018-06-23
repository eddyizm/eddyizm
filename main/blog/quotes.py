import sqlite3
import json
from datetime import datetime as d
# import os.path
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "PupilPremiumTable.db")

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

def send_quote(email, quote, fname ):
  # send via mailgun
  return requests.post(
        "https://api.mailgun.net/v3/mailgun.eddyizm.com/messages",
        auth=("api", "API KEY"),
        data={"from": "Postmaster <postmaster@mailgun.eddyizm.com>",
              "to": [email],
              "subject": "Hello "+ fname,
              "text": "Testing some Mailgun awesomness!"})

def get_email_queue():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row 
  c = conn.cursor()
  rows = c.execute(emailsQueue).fetchall()
  conn.close()
  if len(rows) > 0:
    for r in rows:
      print (r[0]) #
      print (r[1])
      print (r[2])
      print (r[3])
      print (r[4])

def update_hist(date, emailID, quoteID):
  # update Ehistory table with record sent
  pass              

# process 5 emails at a time
def do_the_work():
  pass

#print(get_daily_q())
if __name__ == '__main__':
  get_email_queue()