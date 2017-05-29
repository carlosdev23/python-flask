from flask import Flask
from flask import Flask, render_template, request, json
from  flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash

# define our applications.
app = Flask(__name__)

mysql = MySQL()

# MySQL Configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'localhost'
app.config['MYSQL_DB'] = 'BucketList'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

# route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# route to sign up.
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# server side sign up method
@app.route('/signUp', methods=['POST'])
def signUp ():
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            cur = mysql.connection.cursor()
            _hashed_password = generate_password_hash(_password)
            print _hashed_password
            cur.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cur.fetchall()

            if len( data ) is 0:
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error': str( data[0] )})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})
if __name__ == "__main__":
    app.run()
