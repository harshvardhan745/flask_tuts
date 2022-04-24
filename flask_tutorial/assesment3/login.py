from flask import (Flask, make_response, redirect, render_template, request, url_for, session)

app = Flask(__name__)
app.secret_key = 'alpalpalpalp35678ghdgdhgdhgdh'


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
            session['my_session1'] = uname
            session['my_session2'] = pwd
            return resp
        else:
            return redirect(url_for('error'))


@app.route('/error')
def error():
    return "<h1>error</h1>"


@app.route('/logout')
def logout():
    resp = make_response(render_template('logout.html'))
    session.pop('my_session1', None)
    session.pop('my_session2', None)
    return resp


@app.route('/profile')
def profile():
    uname = session['my_session1']
    return render_template('profile.html', username=uname)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if valid_login(uname, pwd):
            urname = session['my_session1']
            passw = session['my_session2']
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
