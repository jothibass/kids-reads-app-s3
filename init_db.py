from app import create_app, db
from app.models import User, Entry
from flask import current_app

app = create_app()
app.app_context().push()

db.create_all()

def seed_user(username, display_name, password):
    if not User.query.filter_by(username=username).first():
        u = User(username=username, display_name=display_name)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print(f"Created user {username}")

seed_user('jivantika', 'Jivantika', 'Passw0rd!')
seed_user('dikshan', 'Dikshan', 'Passw0rd!')

print('Seeding done.')
