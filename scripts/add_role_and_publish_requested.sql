-- Run this against your Postgres RDS (psql) to add the new columns if not using Flask-Migrate
ALTER TABLE users ADD COLUMN IF NOT EXISTS role varchar(20) DEFAULT 'kid';
ALTER TABLE entries ADD COLUMN IF NOT EXISTS publish_requested boolean DEFAULT false;
