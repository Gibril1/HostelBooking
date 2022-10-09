from flask import request, jsonify
from flask_cors import cross_origin

import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv

from hostel.models.user_models import HostelManager
load_dotenv()

from hostel import db, app
from hostel.models.hostel_models import (
    Hostel,  hostel_schema, hostels_schema,
    HostelFacilities, hostelfacilities_schema,
    HostelRoomType, hostelroomtype_schema
) 

import os

@app.route('/create/hostel/<int:manager_id>', methods=['POST'])
@cross_origin()
def create_hostel(manager_id):
    try:
        response = {
            "data":{},
            "error_message":""
        }

        cloudinary.config(
            cloud_name = os.getenv('CLOUD_NAME'),
            api_key = os.getenv('API_KEY'),
            api_secret = os.getenv('API_SECRET')
        )

        name = request.form['name']
        location = request.form['location']
        rating = request.form['rating']
        image = request.files['image']

        # upload_result=None
        if not name:
            response['error_message']='Name has not been supplied'
            return response, 400

        if image:
            try:
                upload_result = cloudinary.uploader.upload(image)
                # print(upload_result)
            except:
                response['error_message']['image_error'] = 'Image failed to be uploaded. Try again'
        
        hostel_manager = HostelManager.query.get(manager_id=manager_id)
        if not hostel_manager:
            response['error_message'] = f'Manager with id {manager_id} does not exist'
            return response, 404


        hostel = Hostel(name=name, location=location, rating = rating, avatar = upload_result['secure_url'], cloudinary_id = upload_result['public_id'], manager_id=hostel_manager.manager_id)
        db.session.add(hostel)
        db.session.commit()

        hostel = hostel_schema.dump(hostel)
        response['data'] = hostel
        return response, 200
        
    except:
        response['error_message'] = 'Failed to create hostel'
        return response,200


@app.route('/create/facility/<int:hostel_id>', methods=['POST'])
def create_facility(hostel_id):
    response = {
        "data":{},
        "error_message":""
    }

    name = request.form['name']
    image = request.files['image']

    if not name:
            response['error_message']='Name has not been supplied'
            return response, 400

    if image:
        try:
            upload_result = cloudinary.uploader.upload(image)
            # print(upload_result)
        except:
            response['error_message']='Image failed to be uploaded. Try again'
    
    hostel = Hostel.query.get(id=hostel_id)
    if not hostel:
        response['error_message'] = f'Hostel with id {hostel_id} does not exist'
        return response, 404
    
    hostel_facility = HostelFacilities(name=name, avatar = upload_result['secure_url'], cloudinary_id=upload_result['public_url'], hostel_id=hostel.hostel_id)

    db.session.add(hostel_facility)
    db.session.commit()

    hostel_facility = hostelfacilities_schema.dump(hostel_facility)
    response['data'] = hostel_facility
    return response, 200

@app.route('/create/room/<int:hostel_id>', methods=['POST'])
@cross_origin()
def create_room(hostel_id):
    response = {
        "data":{},
        "error_message":""
    }

    data = request.json['data']

    if not data['room_type']:
        response['error_message'] = 'Enter the room type'
        return response, 400

    hostel = Hostel.query.get(id=hostel_id)
    if not hostel:
        response['error_message'] = f'Hostel with id {hostel_id} does not exist'
        return response, 404

    room = HostelRoomType(room_type = data['room_type'], male_bed_space = data['male_bed_space'],available_male_bed_space = data['available_male_bed_space'],female_bed_space = data['female_bed_space'],available_female_bed_space = data['available_female_bed_space'], price=data['price'], hostel_id=hostel.hostel_id)
    db.session.add(room)
    db.session.commit()

    room = hostelroomtype_schema.dump(room)
    response['data'] = room


@app.route('/update/room/<int:room_id>', methods=['PUT'])
@cross_origin()
def update_room(room_id):
    response = {
        "data":{},
        "error_message":""
    }
    
    data = request.json
    room = HostelRoomType.query.get(id=room_id)
    if not room:
        response['error_message'] = 'No such room exists'

    if data['room_type']:
        room.room_type = data['room_type']
    if data['male_bed_space']:
        room.male_bed_space = data['male_bed_space']
    if data['female_bed_space']:
        room.female_bed_space = data['female_bed_space']
    if data['available_male_bed_space']:
        room.available_male_bed_space = data['available_male_bed_space']
    if data['available_female_bed_space']:
        room.available_female_bed_space = data['available_female_bed_space']
    if data['price']:
        room.price = data['price']

    db.session.commit()
    room = hostelroomtype_schema.dump(room)
    response['data'] = room
    return response, 200


@app.route('/delete/room/<int:room_id>', methods=['POST'])
@cross_origin()
def delete_room(room_id):
    response = {
        "data":{},
        "error_message":""
    }

    room = HostelRoomType.query.get(id=room_id)
    if not room:
        response['error_message'] = 'No such room exists'
        return response, 400

    db.session.delete(room)
    db.session.commit()

    room = hostelroomtype_schema(room)
    response['data'] = room.id
    return response, 200

    
@app.route('/get/hostel', methods=['GET'])
def get_hostels():
    response = {
        "data":{},
        "error_message":""
    }

    hostel = Hostel.query.all()
    hostel = hostels_schema.dump(hostel)
    response['data'] = hostel
    return response, 200
    
    