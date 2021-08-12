import youtube_dl
import requests
import sys
import urllib.parse as urlparse
import os
from flaskext.mysql import MySQL

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
