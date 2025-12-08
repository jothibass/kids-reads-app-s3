import os
import boto3
from app import create_app, db
from app.models import Entry
from flask import current_app

app = create_app()
app.app_context().push()

s3 = boto3.client('s3', region_name=app.config['S3_REGION'])
bucket = app.config.get('S3_BUCKET')
upload_folder = app.config['UPLOAD_FOLDER']

if not bucket:
    print("S3_BUCKET not configured. Aborting.")
    raise SystemExit(1)

for e in Entry.query.filter(Entry.photo_filename != None).all():
    v = e.photo_filename
    if v.startswith("local://"):
        fname = v.split("local://",1)[1]
    else:
        fname = v
    local_path = os.path.join(upload_folder, fname)
    if not os.path.exists(local_path):
        print("Missing local file:", local_path)
        continue
    key = f"uploads/{os.path.basename(local_path)}"
    try:
        with open(local_path, 'rb') as fh:
            s3.upload_fileobj(fh, bucket, key, ExtraArgs={'ACL':'private', 'ContentType':'image/jpeg'})
        e.photo_filename = key
        db.session.add(e)
        db.session.commit()
        print("Uploaded and updated:", fname)
    except Exception as exc:
        print("Failed to upload", fname, exc)
print('Migration complete.')
