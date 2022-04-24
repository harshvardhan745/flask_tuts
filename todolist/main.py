from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
app.config['SECRET_KEY'] = "sdfghjkrtyuiiio@#$%^&*SDFGHJFSBWERTYsdcvb$%^"
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    priority = db.Column(db.String(20), nullable=False)

    def __init__(self, title, desc, date_created, email, phone, priority):
        self.title = title
        self.desc = desc
        self.date_created = date_created
        self.email = email
        self.phone = phone
        self.priority = priority


@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        email = request.form['email']
        phone = request.form['phone']
        priority = request.form['priority']
        todo = Todo(title=title, desc=desc, email=email, phone=phone, priority=priority)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/show')
def show():
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        email = request.form['email']
        phone = request.form['phone']
        priority = request.form['priority']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.email = email
        todo.phone = phone
        todo.priority = priority
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
