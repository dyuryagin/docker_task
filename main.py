
from crypt import methods
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
import os
import time

db = os.environ['DB_ADDRESS']
port = os.environ['DB_PORT']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_databasename = os.environ['DB_DATABASENAME']

print('mariadb+pymysql://' + db_user + ':' + db_password + '@' + db + ':' + port + '/' + db_databasename)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://' + db_user + ':' + db_password + '@' + db + ':' + port + '/' + db_databasename
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    comment = db.Column(db.String(120), unique=False, nullable=True)


is_connected = False

while not is_connected:
    try:
        db.create_all()
        is_connected = True
        print("connected")
    except Exception:
        print("sleep 3")
        time.sleep(3)



@app.route('/', methods=['POST','GET'])
def hello_world():
    if request.method == 'GET':
        users = User.query.all()
        answer = ""
        for user in users:
            answer += user.username + " " + user.email + "<br>"
        return answer
    elif request.method == 'POST':
        user_name = request.args.get('user')
        user_email = request.args.get('email')
        user_comment = request.args.get('comment')
        new_user = User(username = user_name, email = user_email, comment = user_comment)
        db.session.add(new_user)
        db.session.commit()
        return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)

