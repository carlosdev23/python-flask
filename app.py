from flask import Flask
from flask import Flask, render_template, request, json
from  flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import Response
from flask import Flask, session, redirect, url_for
import flask_login

# Define our applications.
app = Flask(__name__)

# Secret Key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# MySQL Configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'riksof'
app.config['MYSQL_DB'] = 'BucketList'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# Route to sign up.
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# Route to sign in.
@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

# Route to main.
@app.route('/mains')
def mains():
    if 'username' in session:
        return render_template('mains.html')
    else:
        return redirect( url_for('showSignIn') )
# Server side sign in method
@app.route('/signIn', methods=['POST'])
def signIn():
    try:
        # Read the posted value from UI
        _name = request.form['inputName']
        _password = request.form['inputPassword']

        if _name and _password:
            # Cursor connection
            cur = mysql.connection.cursor()
            # Query execute
            cur.execute("SELECT * FROM tbl_user WHERE user_username = %s AND user_password = %s",[_name, _password])
            data = cur.fetchall()

            if len( data ) is 0:
                # Set response for email duplications
                responseData = json.dumps({'message': 'Invalid UserName and Password.'})
                return Response(responseData, status=400, mimetype='application/json')
            else:
                if request.method == 'POST':
                    session['username'] = _name
                    # return redirect('mains')

                    responseData = json.dumps({'message': 'User Login Successfully.', 'Url': url_for( 'mains')})
                    return Response(responseData, status=200, mimetype='application/json')

    # Exception return.
    except Exception as e:
        return json.dumps({'error': str(e)})

# Server side sign up method
@app.route('/signUp', methods=['POST'])
def signUp ():
    try:
        # Read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Validate the received values.
        if _name and _email and _password:
            # Cursor connection
            cur = mysql.connection.cursor()
            # Query execute
            cur.execute("SELECT * FROM tbl_user WHERE user_email = %s AND user_username = %s",[_email, _name])
            data = cur.fetchall()

            # If user is exist or not.
            if len ( data ) is 0:

                # Insert user Data
                cur.execute("INSERT INTO tbl_user( user_email, user_username, user_password ) VALUES ( %s, %s, %s )",[ _email, _name, _password ])
                mysql.connection.commit()
                # Response data.
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

# Main part.
if __name__ == "__main__":
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
