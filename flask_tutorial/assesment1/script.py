from flask import *

app = Flask(__name__)


@app.route('/success', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if validate_form(request.form['name'], request.form['email'], request.form['contact'],request.form['pin']):
            return render_template("result_data.html", result=request.form)
        else:
            return render_template('customer.html', error='Invalid form')
    return render_template('customer.html')


def validate_form(name, email, contact, pin):
    return name != '' and email != '' and contact != '' and pin != ''


if __name__ == '__main__':
    app.run(debug=True)
