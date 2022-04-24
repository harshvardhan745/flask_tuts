from random import randint
from flask_sqlalchemy import SQLAlchemy
from flask import *
from flask_mail import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SECRET_KEY'] = 'AS62nsfjadsaj_@dfjfsfhbf182sfjdfASFAKSF'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    otp = db.Column(db.String(4))
    verified = db.Column(db.Boolean, default=False, nullable=False)

    def _init_(self, name, email, password, otp, verified):
        self.name = name
        self.email = email
        self.password = password
        self.otp = otp
        self.verified = verified


@app.route('/')
def index():
    return render_template('index.html')


otp = str(randint(0000, 9999))


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    msg = None
    if request.method == 'POST':
        try:
            user = Users(
                request.form['Name'], request.form['Email'], request.form['Password'], otp, False)
            db.session.add(user)
            db.session.commit()
        except:
            return render_template('index.html', msg='Something error happened to database')


        # Flask mail configuration
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'sumit11902960@gmail.com'
        app.config['MAIL_PASSWORD'] = 'Sumit@1234'
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True

        # instantiate the Mail class
        mail = Mail(app)
        email = request.form['Email']
        # configure the Message class object and send the mail from a URL
        msg = Message('OBRS Verification', sender='sumit11902960@gmail.com', recipients=[email])
        msg.body = 'Do not Share This OTP with others - '
        msg.html = '<center><h3>' + str(otp) + '</h3></center>'
        mail.send(msg)

        return render_template('verify.html', msg="Find OTP In Your Mail Box!")

    return render_template('verify.html', msg="Find OTP In Your Mail Box!")


@app.route('/verify1', methods=['GET', 'POST'])
def verify1():
    if request.method == "POST":
        user_otp = request.form['otp']
        if user_otp == otp:
            msg1 = "OTP Verified Successfully!"
            return render_template('verify.html', msg1=msg1)
        else:
            msg1 = "Wrong OTP Entered! _Retry_"
            return render_template('verify.html', msg1=msg1)

    return render_template('verify.html', msg="Find OTP In Your Mail Box!")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)