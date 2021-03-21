from flask import Flask,app, render_template, request, redirect, url_for, flash, session,escape,send_file,abort,send_from_directory
import youtube_dl
import sys
import subprocess
import time
import requests
from helpers.helpers import *
# import pypyodbc
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

### Configuramos la aplicación:

app = Flask(__name__)
app.secret_key = 'so random secret key'
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_SCHEMA')

# Instanciamos la conexión
mysql = MySQL(app)



def my_hook(d):
    if d['status'] == 'finished':
        print('Descarga lista, convirtiendo video...')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

""" ------------------------------------------------- [INDEX] -------------------------------------------------"""
""" [INDEX] """
@app.route('/',methods=['POST','GET'])
def index():
    orig_stdout = sys.stdout
    sys.stdout = open('streams/download.log', 'w')
    sys.stdout.truncate(0)
    download_modes = ["URL única"] #, "start", "add", "list", "delete"]
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        if request.method == 'POST':
            selected_mode  = request.form['mode_selected']
            url_selected  = request.form['url']
            download_folder = request.form['down_folder']
            ydl_opts = {
                    'format': 'best',
                    'outtmpl': download_folder+ '%(title)s.%(ext)s',
                    'nooverwrites': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'newline': True
                    }
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    video_title = ydl.extract_info(url_selected, download=False).get('Title',None)
                    ydl.download([url_selected])
                    print(' Descarga lista en la ruta {}'.format(download_folder))

            except:
                sys.stdout.write('Error, no se permite la descarga desde la fuente...')
            sys.stdout.close()
            orig_stdout = sys.stdout
        variables = {"modes" : download_modes}
        return render_template('index.html', data = variables)
    return redirect(url_for('login'))


@app.route('/login', methods = ['POST', 'GET'])
def login():
    error=None
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        session.pop('username', None)
        if request.method == 'POST':
            username_form  = request.form['username']
            password_form  = request.form['pass']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}';".format(username_form, password_form))
            data = cur.fetchone()
            if data != None:
                session['username']= username_form
                session['password'] = password_form 
                return redirect(url_for('index'))
            else:
                error = "Invalid Credential"
                session.pop('username', None)
    return render_template('login.html', error=error)

""" [METODO QUE PERMITE LEER EL LOG EN REAL TIME] """
@app.route('/stream')
def stream():
    def generate():
        with open('streams/download.log') as f:
            while True:
                yield f.read()
    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)