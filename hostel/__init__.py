from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# Init app
app = Flask(__name__)
# Init cors
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
app.config['SECRET_KEY'] = 'thisisiis'

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
# Init admin
admin = Admin(app)
# Init bcrypt
bcrypt = Bcrypt(app)


from hostel.routes import user_routes, hostel_routes
