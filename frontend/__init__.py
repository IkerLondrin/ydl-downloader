from flask import Flask, render_template, request, redirect, url_for, flash, session,escape,send_file,abort,send_from_directory
import youtube_dl
import sys
import subprocess
import time



app = Flask(__name__)
app.secret_key = 'so random secret key'

def my_hook(d):
    if d['status'] == 'finished':
        print('Descarga lista, convirtiendo video...')

""" ------------------------------------------------- [INDEX] -------------------------------------------------"""
""" [INDEX] """
@app.route('/',methods=['POST','GET'])
def index():
    download_modes = ["custom"] #, "start", "add", "list", "delete"]
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
                    'newline': True,
                    # 'progress_hooks': [my_hook]
                    }
            sys.stdout = open('streams/download.log', 'w')
            sys.stdout.truncate(0)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_selected])
                print(' Descarga lista en la ruta {}'.format(download_folder))
            sys.stdout.close()
            sys.stdout = sys.__stdout__
        return render_template('index.html', modes = download_modes)
    return redirect(url_for('login'))


@app.route('/login', methods = ['POST', 'GET'])
def login():
    error=None
    session.pop('username', None)
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            username_form  = request.form['username']
            password_form  = request.form['pass']
            if (username_form == "prueba" and password_form == "pruebapwd"):
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