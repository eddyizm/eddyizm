import sqlite3
import json
from datetime import datetime as d
# import os.path
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "PupilPremiumTable.db")

# queries
insertQuoteH = 'INSERT INTO QuoteHistory VALUES (?, ?)'
sqlite_file = 'main/quotes_app.sqlite3'

# return random quote
def get_random_q():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row 
  c = conn.cursor()
  rows = c.execute('''select quote, ID from randomQview''').fetchall()
  conn.close()
  return json.dumps( [dict(ix) for ix in rows] )   
#return json.dumps(dict(c.fetchall()))

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
  #print (rows[1])
  
# conn.commit()

#insert_daily_q()