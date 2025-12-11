from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # If your table uses 'username' keep it; if it uses 'name', keep that too.
    # Include both if you want to support either (they can both map to DB cols if present).
    username = db.Column(db.String(80), unique=True, nullable=True)   # optional, keep if your app uses it
    name = db.Column(db.String(80), nullable=True)                     # optional, keep if your DB has 'name'
    display_name = db.Column(db.String(120), nullable=True)

    # *** Add this email column to match the RDS schema (NOT NULL in your DB) ***
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='kid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(200))
    type = db.Column(db.String(20))
    notes = db.Column(db.Text)
    photo_filename = db.Column(db.String(255))
    interest_tags = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=False)       # visible to public
    publish_requested = db.Column(db.Boolean, default=False) # kids request
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

