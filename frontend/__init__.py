from flask import Flask, render_template, request, redirect, url_for, flash, session,escape,send_file,abort,send_from_directory
app = Flask(__name__)
app.secret_key = 'so random secret key'



""" ------------------------------------------------- [INDEX] -------------------------------------------------"""
""" [INDEX] """
@app.route('/',methods=['POST','GET'])
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html')
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
                session['password'] = password_form #password_form
                return redirect(url_for('index'))
            else:
                error = "Invalid Credential"
                session.pop('username', None)
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)