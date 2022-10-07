
from flask import request
from hostel import app, bcrypt, db
from hostel.models import Tenant, tenant_schema

import jwt
import datetime

@app.route('/register', methods=['POST'])
def register():
    # try:
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

        tenant = Tenant.query.filter_by(username=data['username']).first()
        if tenant:
            response['error_message'] = 'Tenant account already exists. Login'
            return response, 301

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        print(hashed_password)
        tenant = Tenant(username=data['username'], email_address=data['email_address'], password=hashed_password)
        db.session.add(tenant)
        db.session.commit()

        tenant = tenant_schema.dump(tenant)
        response["data"] = tenant

        return response, 200

    # except:
    #     response['error_message'] = 'No such user'
    #     return response, 500


@app.route('/login', methods=['POST'])
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

        tenant = Tenant.query.filter_by(username=username).first()
        if tenant and bcrypt.check_password_hash(tenant.password, password):
            token = jwt.encode({'tenant':tenant.username,'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            tenant = tenant_schema.dump(tenant)
            response["auth_token"] = token
            response["data"] = tenant
            return response, 200
        else:
            response['error_message'] = 'Invalid Credentials/ No such user'
            return response, 404


        
    except:
        response['error_message'] = 'Error'
        return response, 500
