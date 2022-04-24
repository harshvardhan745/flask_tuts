from flask import Flask, escape


app = Flask(__name__)


# routes with variable path
@app.route('/user/<username>')
def display_username(username):
    return f"hi {escape(username)}"

@app.route('/user/<username>')
def success(username):
    return f"sucess..."

@app.route('/user/<username>')
def fail(username):
    return f"sucess..."


if __name__ == '__main__':
    app.run(debug=True)