#from .model import Model_Class
from flask import request, jsonify, session, Blueprint
import hashlib

login_bp = Blueprint('login_bp', __name__)

#model = Model_Class()

@login_bp.route('/user/login', methods=['POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        hash = hashlib.sha1(password.encode())
        password = hash.hexdigest()
        # If account exists in accounts table in out database
#        account = model.login_user(username,password)
#        if account:
            # Create session data, we can access this data in other routes
#            session['loggedin'] = True
#            msg = 'Logged in successfully!'
#        else:
            # Account doesnt exist or username/password incorrect
#            msg = 'Incorrect username/password!'
    response = {'message': msg}
    return jsonify(response)