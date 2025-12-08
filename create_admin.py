from app import create_app, db
from app.models import User
app = create_app()
app.app_context().push()
username = 'admin'
password = 'AdminPassw0rd!'
u = User.query.filter_by(username=username).first()
if u:
    print("Admin already exists.")
else:
    u = User(username=username, display_name='Admin')
    u.set_password(password)
    u.role = 'admin'
    db.session.add(u)
    db.session.commit()
    print(f"Created admin user '{username}' with password '{password}' -- change password immediately.")
