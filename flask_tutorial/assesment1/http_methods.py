from flask import Flask, render_template, request

app = Flask(__name__)


#Request and response
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if valid_login(uname, pwd):
            if uname == 'harsh' and pwd == '1234':
                return render_template("succ.html", error1="login success...")
            else:
                return render_template("error.html", error2="login failure...")
        else:
            return render_template("error.html", error2="please enter username and password")
    return render_template('login.html')


def valid_login(username, password):
    return username != '' and password != ''


if __name__ == '__main__':
    app.run(debug=True)