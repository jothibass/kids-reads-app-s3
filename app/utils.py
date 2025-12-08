import io
import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app
import boto3
from botocore.exceptions import ClientError
import mimetypes

def allowed_file(filename):
    ext = filename.rsplit('.',1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config['ALLOWED_EXTENSIONS']

def _get_s3_client():
    session = boto3.session.Session(region_name=current_app.config.get('S3_REGION'))
    return session.client('s3')

def save_photo(file):
    if not file:
        return None

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.',1)[-1].lower()
    key = f"uploads/{uuid.uuid4().hex}.{ext}"

    # create a thumbnail in-memory to avoid huge files
    try:
        img = Image.open(file)
        img.thumbnail((1600, 1600))
        buf = io.BytesIO()
        fmt = 'JPEG' if ext in ['jpg', 'jpeg'] else ext.upper()
        img.save(buf, format=fmt)
        buf.seek(0)
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    except Exception:
        file.stream.seek(0)
        buf = io.BytesIO(file.read())
        buf.seek(0)
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    if current_app.config.get('USE_S3', True) and current_app.config.get('S3_BUCKET'):
        s3 = _get_s3_client()
        bucket = current_app.config['S3_BUCKET']
        try:
            s3.upload_fileobj(
                Fileobj=buf,
                Bucket=bucket,
                Key=key,
                ExtraArgs={
                    "ContentType": content_type,
                    "ACL": "private"
                }
            )
            return key
        except ClientError as e:
            current_app.logger.error("Failed to upload to S3: %s", e)
            return None
    else:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        local_name = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(upload_folder, local_name)
        with open(path, "wb") as f:
            f.write(buf.getbuffer())
        return f"local://{local_name}"
