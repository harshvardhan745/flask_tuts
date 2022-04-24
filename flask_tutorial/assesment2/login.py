from flask import (Flask, make_response, redirect, render_template, request,url_for)

app = Flask(__name__)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        if pwd != '':
            resp = make_response(render_template('success.html'))
            resp.set_cookie('username', uname)
            resp.set_cookie('password', pwd)
            return resp
        else:
            return redirect(url_for('error'))


@app.route('/error')
def error():
    return "<h1>error</h1>"

@app.route('/profile')
def profile():
    uname = request.cookies.get('username')
    return render_template('profile.html', username=uname)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if valid_login(uname, pwd):
            urname = request.cookies.get('username')
            passw = request.cookies.get('password')
            if uname == urname and pwd == passw:
                return render_template('profile.html')
            else:
                return redirect(url_for('error'))
        else:
             return redirect(url_for('error'))
    return render_template('login.html')

def valid_login(username, password):
    return username != '' and password != ''

if __name__ == '__main__':
    app.run(debug=True)