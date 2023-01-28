from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

app.secret_key = 'asdfghjklm'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Current-Root-Password'
app.config['MYSQL_DB'] = 'newtestdb'

mysql = MySQL(app)