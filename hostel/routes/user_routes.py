
from flask import request
from flask_cors import cross_origin
from hostel import app, bcrypt, db
from hostel.models.user_models import HostelManager, StudentProfile, User, studentprofile_schema, hostelmanger_schema

import jwt
import datetime

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    try:
        response = {
            "data":{},
            "error_message":""
        }
        data = request.json['data']
        print(data)

        if not data['username']:
            response['error_message'] = 'Username has not been provided'
            return response, 404
        if not data['password']:
            response['error_message'] = 'Password has not been provided'
            return response, 404

        user = User.query.filter_by(username=data['username']).first()
        if user:
            response['error_message'] = 'User account already exists. Login'
            return response, 301

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(username=data['username'], email_address=data['email_address'], password=hashed_password, role=data['role'])
        db.session.add(user)
        db.session.commit()


        if user.role == 'student':
            student_profile = StudentProfile(reference_number=data['reference_number'], user = user.id, first_name = data['first_name'], last_name=data['last_name'], other_names=data['other_name'], phone_number = data['phone_number'], program_of_study = data['program_of_study'], gender = data['gender'])
            db.session.add(student_profile)
            db.session.commit()

            student_profile = studentprofile_schema.dump(student_profile)
            response["data"] = student_profile

            return response, 200

        elif user.role == 'manager':
            hostel_manager = HostelManager(user = user.id, first_name = data['first_name'], last_name=data['last_name'], other_name=data['other_name'], phone_number = data['phone_number'], program_of_study = data['program_of_study'], gender = data['gender'])
            db.session.add(hostel_manager)
            db.session.commit()

            
            hostel_manager = hostelmanger_schema.dump(hostel_manager)
            response["data"] = hostel_manager
            return response, 200

    except:
        response['error_message'] = 'Error'
        return response, 500


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        response = {
            "data":{},
            "error_message":""
        }

        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            response['error_message'] = 'Username has not been provided'
            return response, 404
        if not password:
            response['error_message'] = 'Password has not been provided'
            return response, 404

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'user':user.username,'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        
        if user.role == 'student':
            studentprofile = StudentProfile.query.filter_by(user=user.id).first()
            studentprofile = studentprofile_schema.dump(studentprofile)
            response["auth_token"] = token
            response["data"] = studentprofile
            return response, 200

        elif user.role == 'manager':
            hostelmanager = HostelManager.query.filter_by(user=user.id).first()
            hostelmanager = hostelmanger_schema.dump(hostelmanager)
            response["auth_token"] = token
            response["data"] = hostelmanager
            return response, 200
        else:
            response['error_message'] = 'Invalid Credentials/ No such user'
            return response, 404
        
       
        

        
    except:
        response['error_message'] = 'Error'
        return response, 500
