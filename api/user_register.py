from flask_bcrypt import Bcrypt
from flask import request, jsonify, Blueprint,session
#from .model import Model_Class

register_bp = Blueprint('register_bp', __name__)
bcrypt = Bcrypt(register_bp)
#model = Model_Class()

@register_bp.route('/user/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.json["password"]
    email = request.json["email"]

#    user_exists = model.fetch_user_cred_details(email)

#    if user_exists:
#        return jsonify({"error": "User already exists"}), 409

#    hashed_password = bcrypt.generate_password_hash(password)
#    new_user = model.insert_user_cred_details(email,username,hashed_password)
#    model.session.add(new_user)
#    model.session.commit()
    
#    session["user_id"] = new_user.id

    return jsonify({"Message": "Account created"}), 200