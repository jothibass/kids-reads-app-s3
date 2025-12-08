import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_this_super_secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join('instance','kidsreads.sqlite3')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024


# S3 settings
