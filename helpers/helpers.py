import youtube_dl
import requests
import sys
import urllib.parse as urlparse
# import sqlite3
import os
from flaskext.mysql import MySQL
# from prettytable import PrettyTable
# from sqlite3 import Error
# import requests
# from bs4 import BeautifulSoup

def ph_url_check(url):
    parsed = urlparse.urlparse(url)
    regions = ["www", "cn", "cz", "de", "es", "fr", "it", "nl", "jp", "pt", "pl", "rt"]
    for region in regions:
        if parsed.netloc == region + ".pornhub.com":
            print(" Url de PH validad...")
            return
    print(" Error, no es un video de PH.")
    sys.exit()

def check_login(username, password):
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(1) FROM usuarios WHERE user = {} AND password = {};".format(username, password))
    # if cur.fetchone()[0]:
    #     return True
    # else:
    #     return False
    if username == "username" and password == "password":
        return True
    else:
        return False
