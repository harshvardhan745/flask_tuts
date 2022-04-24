from datetime import datetime, timezone
from pytz import timezone
from flask import Flask, request, render_template,redirect

app = Flask(__name__)


# Request and Response
@app.route('/time', methods=['GET', 'POST'])
def time():
    if request.method == 'POST':
        timez = request.form['timez']

        if request.form['timez'] == '':
            return render_template('home.html', error='Enter Time Zone! e.g. ')
        elif request.form['timez'] == 'Asia/Kolkata':
            return render_template('home.html', DateTime=datetime.now(timezone(timez)))
        elif request.form['timez'] == 'Asia/Kolkata':
            return render_template('home.html', DateTime=datetime.now(timezone(timez)))
        else:
            return render_template('home.html', error='Enter Correct Time Zone e.g.  ')


    return render_template('time.html')


if __name__ == '_main_':
    app.run(debug=True)