# Kids Reads App

Simple Flask app for kids to record books, trips, activities, upload photos, and publish entries.

## Quick start (EC2)

1. Clone repo on EC2.
2. Create a Python venv and install requirements:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set environment variables (example):
   ```
   export SECRET_KEY=change_me
   export DATABASE_URL=postgresql://dbuser:dbpass@rds-hostname:5432/kidsreads
   export UPLOAD_FOLDER=/var/www/kids-reads-app/uploads
   ```
   If `DATABASE_URL` is not set the app uses a local SQLite DB at `instance/kidsreads.sqlite3`.
4. Initialize DB and seed sample users:
   ```
   source venv/bin/activate
   python init_db.py
   ```
   This creates two users:
   - Username: jivantika  Password: Passw0rd!
   - Username: dikshan    Password: Passw0rd!
5. Start with gunicorn for production testing:
   ```
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```
6. Configure nginx and systemd as needed.

## Notes
- For production use RDS Postgres and S3 for uploads. Use HTTPS (Certbot).


## Auto-deploy via GitHub Actions
Files added: `.github/workflows/deploy-to-ec2.yml`, `deploy_scripts/remote_deploy.sh`.
Set repository secrets: EC2_HOST, EC2_SSH_KEY, EC2_USER, EC2_DEPLOY_PATH
