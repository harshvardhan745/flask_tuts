from datetime import datetime, timezone

import pytz
from pytz import timezone
from flask import Flask, request, render_template,redirect
from werkzeug.datastructures import Range

app = Flask(__name__)


# Request and Response
@app.route('/time', methods=['GET', 'POST'])
def time():
    if request.method == 'POST':
        timez = request.form['timez']

        if request.form['timez'] == '':
            return render_template('time.html', error='Enter Time Zone!')
        else:
            try:
                timez1 = pytz.timezone(timez)
                return render_template('time.html', timez=timez1, DateTime=datetime.now(timezone(timez)))
            except:
                return render_template('time.html', error='Enter Valid Time Zone')

    return render_template('time.html')


if __name__ == '__main__':
    app.run(debug=True)