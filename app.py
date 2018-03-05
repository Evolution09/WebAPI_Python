from flask import Flask, request, json
from flaskext.mysql import MySQL

mysql = MySQL();
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zaq12345'
app.config['MYSQL_DATABASE_DB'] = 'sys'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/signUp', methods=['POST'])
def signUp():
    #asdsa


if __name__ == '__main__':
    app.run(debug=True)

