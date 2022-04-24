from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite3'
app.config['SECRET_KEY'] = 'AS62nsfjadsaj_@dfjfsfhbf182sfjdfASFAKSF'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column(db.String)
    name = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True, nullable=True)
    phone = db.Column(db.String(10), unique=True, nullable=True)
    priority = db.Column(db.String(15))

    def __init__(self, date, name, email, phone, pri):
        self.date = date
        self.name = name
        self.email = email
        self.phone = phone
        self.priority = pri


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    msg: None = None
    if request.method == 'POST':
        # try:
        todo = Todo(request.form['date'], request.form['name'], request.form['email'], request.form['phone'],
                    request.form['pri'])
        db.session.add(todo)
        db.session.commit()

        msg = "Task Added Successfully!"
        print(msg)
        return render_template('index.html', msg=msg)
    # except:
    else:
        msg = 'Error Adding Task'
        return render_template('index.html', msg=msg)

    return render_template('index.html', msg=msg)


@app.route('/list')
def list():
    return render_template('list.html', todos=Todo.query.all())


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.filter_by(id=id).first()

    if request.method == 'POST':
        try:
            todo.Task_Date = request.form['date']
            todo.Task_Name = request.form['name']
            todo.Task_Email = request.form['email']
            todo.Task_Phone = request.form['phone']
            todo.Task_Priority = request.form['pri']

            db.session.commit()
            msg = 'Task Updated!'
            return render_template('edit.html', msg=msg, todo=todo)
        except:
            msg = 'Task Updation Failed!'
            return render_template('edit.html', msg=msg, todo=todo)
    else:
        return render_template('edit.html', todo=todo)


@app.route('/delete/<id>')
def delete(id):
    try:
        Todo.query.filter_by(id=id).delete()
        db.session.commit()
        msg = 'Task Deleted SuccessFully'
        return render_template('list.html', msg=msg, todos=Todo.query.all())
    except:
        flash('Unable to delete!')

    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
