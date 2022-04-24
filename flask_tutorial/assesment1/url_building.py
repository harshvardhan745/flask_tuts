from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/success')
def success():
    return "<h1>User Login Success!<h1>"


@app.route('/failed')
def failed():
    return "<h1>User Login Failed!<h1>"


@app.route('/login/<username>')
def login(username):
    if username == 'john':
        return redirect(url_for('success'))
    else :
        return redirect(url_for('failed'))


if __name__ == '__main__':
    app.run(debug=True)