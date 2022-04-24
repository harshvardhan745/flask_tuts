from flask import Flask
from flask_mail import *

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sumit11902960@gmail.com'
app.config['MAIL_PASSWORD'] = 'Sumit@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)


@app.route('/')
def index():
    for i in range(100):
        msg = Message('My subject', sender='sumit11902960@gmail.com',
                      recipients=['rahuladhikari21@gmail.com'])
        msg.body = 'hi, how are you doing... This is sumit'
        msg.html='<h2>heteubjksdjb</h2>'
        mail.send(msg)

    return 'Mail sent. Thanks.'


if __name__ == '__main__':
    app.run(debug=True)