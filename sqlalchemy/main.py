from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient.sqlite3'
app.config['SECRET_KEY'] = 'AS62nsfjadsaj_@dfjfsfhbf182sfjdfASFAKSF'

db = SQLAlchemy(app)


class Patient(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.String(100))

    def __init__(self, name, gender, age, address):
        self.name = name
        self.gender = gender
        self.age = age
        self.address = address


@app.route('/')
def index():
    return render_template('list.html', patient=Patient.query.all())


@app.route('/add', methods=['GET', 'POST'])
def add():
    msg = None
    if request.method == 'POST':
        try:
            patient = Patient(
                request.form['name'], request.form['gender'], request.form['age'], request.form['address'])
            db.session.add(patient)
            db.session.commit()

            flash('Patient addition successful')
            return redirect(url_for('index'))
        except:
            msg = 'Error adding patient'

    return render_template('add.html', msg=msg)


@app.route('/delete/<id>')
def delete(id):
    try:
        Patient.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Deletion successful')
    except:
        flash('Unable to delete!')

    return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    patient = Patient.query.filter_by(id=id).first()

    if request.method == 'POST':
        try:
            patient.name = request.form['name']
            patient.gender = request.form['gender']
            patient.age = request.form['age']
            patient.address = request.form['address']
            db.session.commit()

            flash('Update successful')
        except:
            flash('Error updating Patient!')

        return redirect(url_for('index'))
    else:
        return render_template('edit.html', patient=patient)


if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)
