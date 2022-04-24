import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'W_1f$sjfdf72masbasdjad^63MSDFKajow9102SFjfsl'


MY_DB = 'students.db'

def init_db():
    con = sqlite3.connect(MY_DB)

    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            student_name TEXT NOT NULL, 
            class_name TEXT NOT NULL, 
            roll_no TEXT NOT NULL
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
            sname = request.form['student_name']
            sclass = request.form['class_name']
            sroll = request.form['roll_no']

            with sqlite3.connect(MY_DB) as conn:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO students (student_name, class_name, roll_no) VALUES (?,?,?)', (sname, sclass, sroll))

                conn.commit()

                msg = 'Student creation successful!'
        except:
            conn.rollback()
            msg = 'Error creating student'
        finally:
            conn.close()

    return render_template('create.html', msg=msg)


@app.route('/view')
def read():
    conn = sqlite3.connect(MY_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    rows = cur.fetchall()

    conn.close()

    return render_template('view.html', rows=rows)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    msg = None
    row = None

    with sqlite3.connect(MY_DB) as conn:
        if request.method == 'POST':
            sname = request.form['student_name']
            cname = request.form['class_name']
            rno = request.form['roll_no']

            cur = conn.cursor()

            try:
                cur.execute(
                    'UPDATE students SET student_name=?, class_name=?, roll_no=? WHERE id = ?', (sname, cname, rno, id))

                conn.commit()
                return redirect(url_for('read'))
            except:
                conn.rollback()
                msg = 'Error updating rerord'

        else:
            try:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('SELECT * FROM students WHERE id=?', id)
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
            cur.execute('DELETE FROM students WHERE id=?', id)
            msg = 'Deletion successful'
        except:
            msg = 'Deletion failed'
        finally:
            flash(msg)
            return redirect(url_for('read'))


init_db()

if __name__ == '__main__':
    app.run(debug=True)