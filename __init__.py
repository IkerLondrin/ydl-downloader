from flask import Flask,app, render_template, request, redirect, url_for, flash, session,escape,send_file,abort,send_from_directory
import youtube_dl
import sys
import subprocess
import time
import requests
from helpers.helpers import *
#import pypyodbc
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
from datetime import timedelta
import os
from dotenv import load_dotenv
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')



app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_SCHEMA')


mysql = MySQL(app)



def my_hook(d):
    if d['status'] == 'finished':
        print('Descarga lista, convirtiendo video...')

@app.before_request
def make_session_permanent():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=1)

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
                    'outtmpl': download_folder+'/'+ '%(id)s_%(title)s.%(ext)s',
                    'nooverwrites': False,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'newline': True
                    }
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(url_selected, download=False)
                    ydl.download([url_selected])
                path = download_folder + '/' + video_info.get('id',None) + '_' +  video_info.get('title',None) + '.' + video_info.get('ext', None)
                sys.stdout.write('Iniciando la descarga del video...')
                time.sleep(2)
                try:
                    directory = os.listdir(download_folder+'/')
                    for file in directory:
                        if file.startswith(video_info.get('id',None)):
                            filename_new = str(file).replace('!', '')
                            renamed = os.path.join(download_folder, filename_new)
                            os.rename(os.path.join(download_folder, file), os.path.join(download_folder, filename_new))
                    return send_file(renamed, as_attachment=True)
                except Exception as e:
                    print('Excepcion sin renombrar: ', e)
                    sys.stdout.write('No se ha podido descargar el video...')
            except Exception as e:
                print('Exception: ', e)
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
            try:
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
            except:
                error = "No ha sido posible verificar..."
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
    app.run(debug=False,host= '0.0.0.0')
