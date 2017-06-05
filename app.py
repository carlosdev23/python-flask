from flask import Flask
from flask import Flask, render_template, request, json
from  flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import Response

# define our applications.
app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'riksof'
app.config['MYSQL_DB'] = 'BucketList'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

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

        # validate the received values.
        if _name and _email and _password:
            # cursor connection
            cur = mysql.connection.cursor()
            # query execute
            cur.execute("SELECT * FROM tbl_user WHERE user_email = %s",[_email])
            data = cur.fetchall()

            # if user is exist or not.
            if len ( data ) is 0:
                # insert user Data
                cur.execute("INSERT INTO tbl_user( user_email, user_username, user_password ) VALUES ( %s, %s, %s )",[ _email, _name, _password ])
                mysql.connection.commit()
                # response data.
                responseData = json.dumps({'message':'User created successfully.'})
                return Response(responseData, status=200, mimetype='application/json')

            else:
                # Set response for email duplications
                responseData = json.dumps({'message': 'Email address is already used.'})
                return Response(responseData, status=400, mimetype='application/json')
        else:
            # Set repsonse for sign up form validation
            responseData = json.dumps({'message':'Enter the required fields'})
            return Response( responseData, status=400, mimetype='application/json')
    # Exception occur
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
