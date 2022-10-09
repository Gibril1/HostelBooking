
from hostel import db, ma



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email_address = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(20), nullable = False)
    role = db.Column(db.String(20), nullable = False, default='student')

    student = db.relationship('StudentProfile', backref='studentprofile', lazy = True)
    manager = db.relationship('HostelManager', backref='studentprofile', lazy = True)

    def __repr__(self):
        return f'User {self.username} - {self.email_address}'

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email_address', 'role')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

class StudentProfile(db.Model):
    reference_number = db.Column(db.String(20), primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    other_names = db.Column(db.String(20))
    phone_number = db.Column(db.String(20), nullable = False)
    program_of_study = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self) -> str:
        return f'Student f{self.reference_number} - {self.program_of_study}'

class StudentProfileSchema(ma.Schema):
    class Meta:
        fields=('reference_number', 'user', 'first_name', 'last_name', 'other_names', 'phone_number', 'program_of_study', 'gender')

studentprofile_schema = StudentProfileSchema()
studentprofiles_schema = StudentProfileSchema(many=True)

class HostelManager(db.Model):
    __tablename__ = 'hostelmanager'
    manager_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    other_names = db.Column(db.String(20))
    phone_number = db.Column(db.String(20), nullable = False)
    program_of_study = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    hostel_manager = db.relationship('Hostel', backref = 'manager', lazy = True)

    def __repr__(self):
        return f'Manager {self.manager_id} - {self.user}'
    


class HostelManagerSchema(ma.Schema):
    class Meta:
        fields=('manager_id', 'user', 'first_name', 'last_name', 'other_names', 'phone_number', 'program_of_study', 'gender')

hostelmanger_schema = HostelManagerSchema()
hostelmanagers_schema = HostelManagerSchema(many=True)




