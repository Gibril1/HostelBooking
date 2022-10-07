from hostel import db, ma

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email_address = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f'Tenant {self.username} - {self.email_address}'

class TenantSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email_address')

tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many = True)