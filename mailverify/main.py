from random import randint
from flask_sqlalchemy import SQLAlchemy
from flask import *
from flask_mail import *
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, validators

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = 'AS62nsfjadsaj_@dfjfsfhbf182sfjdfASFAKSF'

# Flask mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sumit11902960@gmail.com'
app.config['MAIL_PASSWORD'] = 'Sumit@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    otp = db.Column(db.String(4))
    verified = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, email, password, otp, verified):
        self.name = name
        self.email = email
        self.password = password
        self.otp = otp
        self.verified = verified


@app.route('/')
def index():
    return render_template('index.html')


otp = str(randint(1000, 9999))

mail = Mail(app)


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    msg = None
    if request.method == 'POST':
        user = Users(
            request.form['Name'], request.form['Email'], request.form['Password'], otp, False)
        db.session.add(user)
        db.session.commit()

        email = request.form['Email']
        msg = Message('Verification', sender='sumit11902960@gmail.com', recipients=[email])
        msg.body = 'Do not Share This OTP with others - '
        msg.html = '<center><h3>' + str(otp) + '</h3></center>'
        mail.send(msg)

        return render_template('verify.html', msg="Find OTP In Your Mail Box!")

    return render_template('verify.html', msg="Find OTP In Your Mail Box!")


class UserForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired('Please enter user name')])
    email = StringField('Email',[validators.DataRequired('Please enter your email')])
    password = StringField('Password', [validators.DataRequired('Please enter your password')])
    submit = SubmitField('Submit')


@app.route('/verify1', methods=['GET', 'POST'])
def verify1():
    form = UserForm()
    if request.method == "POST":
        user_otp = request.form['otp']
        if user_otp == otp:
            user = Users.query.filterby()
            msg1 = "OTP Verified Successfully!"
            return msg1
        else:
            msg1 = "Wrong OTP Entered! _Retry_"
            return msg1

    return render_template('verify.html', msg="Find OTP In Your Mail Box!")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
