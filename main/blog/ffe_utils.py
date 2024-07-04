import sqlite3
import requests
import os
from datetime import datetime as d
from django.conf import settings

api_key = settings.MAILGUN_KEY


def update_FFE(version: str, URL: str):
    ''' Update version available for app to check
    DEPRECATE
    '''
    updateFFEVersion = "UPDATE FFEAppVersion SET DateUpdated = ?, Version = ?, URL = ? WHERE AppName = 'FlatFileExporter';"
    # currDate = d.now().strftime("%Y-%m-%d")
    # with sqlite3.connect(sqlite_file) as conn:
    #     c = conn.cursor()
    #     c.execute(updateFFEVersion, (currDate, version, URL))
    #     conn.commit()


def get_FFE():
    ''' Get version and url '''
    getFFEVersion = "select Version, DateUpdated, URL from FFEAppVersion;"
    #   with sqlite3.connect(sqlite_file) as conn:
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     rows = c.execute(getFFEVersion).fetchall()
    #     data = {"Version": rows[0][0],
    #           "DateUpdated": rows[0][1],
    #           "URL": rows[0][2] }
    #   return data


def get_daily_q():
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://ragingdharma.com/api/v1/daily/', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            'quote': data.get('quote'),
            'dateSent': '',
            'quoteID_FK': data.get('id'),
            'category': data.get('category')
        }


def get_random_q():
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://ragingdharma.com/api/v1/random/', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "quote": data.get('quote'),
            "ID": data.get('id')
        }


def send_message(message):
    return requests.post(
        "https://api.mailgun.net/v3/mg.eddyizm.com/messages",
        auth=("api", api_key),
        data={"from": "Postmaster <postmaster@mg.eddyizm.com>",
              "to": 'eddyizm@gmail.com',
              "subject": "Website Inquiry",
              "text": message
              })
