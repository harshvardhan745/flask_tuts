import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'W_1f$sjfdf72masbasdjad^63MSDFKajow9102SFjfsl'

MY_DB = 'patient.db'


def init_db():
    con = sqlite3.connect(MY_DB)

    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            gender TEXT NOT NULL, 
            age INTEGER NOT NULL,
            address TEXT NOT NULL
        )
        '''
    )

    con.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    msg = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            gender = request.form['gender']
            age = request.form['age']
            address = request.form['address']

            with sqlite3.connect(MY_DB) as conn:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO patient (name, gender, age, address) VALUES (?,?,?,?)', (name, gender, age, address))
                conn.commit()

                msg = 'Patient creation successful!'
        except:
            conn.rollback()
            msg = 'Error creating patient'
        finally:
            conn.close()

    return render_template('create.html', msg=msg)


@app.route('/view')
def read():
    conn = sqlite3.connect(MY_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM patient')
    rows = cur.fetchall()

    conn.close()

    return render_template('view.html', rows=rows)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    msg = None
    row = None

    with sqlite3.connect(MY_DB) as conn:
        if request.method == 'POST':
            name = request.form['name']
            gender = request.form['gender']
            age = request.form['age']
            address = request.form['address']

            cur = conn.cursor()

            try:
                cur.execute(
                    'UPDATE patient SET name=?, gender=?, age=?, address=? WHERE id = ?',
                    (name, gender, age, address, id))

                conn.commit()
                return redirect(url_for('read'))
            except:
                conn.rollback()
                msg = 'Error updating record'

        else:
            try:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('SELECT * FROM patient WHERE id=?', id)
                row = cur.fetchone()
            except:
                flash('No record found')
                return redirect(url_for('read'))

    return render_template('edit.html', msg=msg, row=row)


@app.route('/delete/<id>')
def delete(id):
    msg = None
    with sqlite3.connect(MY_DB) as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM patient WHERE id=?', id)
            msg = 'Deletion successful'
        except:
            msg = 'Deletion failed'
        finally:
            flash(msg)
            return redirect(url_for('read'))


init_db()

if __name__ == '__main__':
    app.run(debug=True)
