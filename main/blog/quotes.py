import sqlite3
import json
# import os.path
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "PupilPremiumTable.db")
# return random quote
sqlite_file = 'main/quotes_app.sqlite3'

def get_random_q():
  conn = sqlite3.connect(sqlite_file)
  conn.row_factory = sqlite3.Row 
  c = conn.cursor()
  rows = c.execute('''select quotes.quote AS quote,quotes.ID AS ID from quotes
              WHERE quotes.ID = (SELECT ABS(RANDOM()) % (5245 - 1) + 1)''').fetchall()
  conn.close()
  return json.dumps( [dict(ix) for ix in rows] )   
#return json.dumps(dict(c.fetchall()))
  
#data = c.fetchall()
# conn.commit()
#print (json.dumps(c.fetchone()))   
# 
# 
#print (get_random_q())