from hostel import db, ma

class Hostel(db.Model):
    hostel_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique = True)
    location = db.Column(db.String(20))
    rating = db.Column(db.Integer)
    avatar= db.Column(db.String(200))
    cloudinary_id= db.Column(db.String(200))
    manager_id = db.Column(db.Integer, db.ForeignKey('hostelmanager.id'))
    
    facilities = db.relationship('HostelFacilities', backref='facility', lazy=True)
    room_type = db.relationship('HostelRoomType', backref='type', lazy=True)
    

class HostelSchema(ma.Schema):
    class Meta:
        fields=('hostel_id','name', 'location', 'rating', 'avatar', 'cloudinary_id')

hostel_schema = HostelSchema()
hostels_schema = HostelSchema(many=True)


class HostelFacilities(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    avatar = db.Column(db.String(200))
    cloudinary_id = db.Column(db.String(200))

    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.hostel_id'))


class HostelFacilitiesSchema(ma.Schema):
    class Meta:
        fields = ('name', 'avatar', 'cloudinary_id')

hostelfacilities_schema = HostelFacilitiesSchema(many=True)


class HostelRoomType(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    room_type=db.Column(db.Integer, nullable = False)
    male_bed_space=db.Column(db.Integer)
    available_male_bed_space=db.Column(db.Integer)
    female_bed_space=db.Column(db.Integer)
    available_female_bed_space=db.Column(db.Integer)
    price = db.Column(db.Float)

    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.hostel_id'))

class HostelRoomTypeSchema(ma.Schema):
    class Meta:
        fields = ('room_type', 'available_male_bed_space', 'available_female_bed_space', 'price')


hostelroomtype_schema = HostelRoomTypeSchema()
hostelroomtypes_schema = HostelRoomTypeSchema(many=True)
