from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegisterForm, LoginForm, EntryForm
from app.models import User, Entry
from app import db
from app.utils import save_photo
import os
import boto3
from botocore.exceptions import ClientError
from flask import redirect, abort

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    entries = Entry.query.filter_by(published=True).order_by(Entry.created_at.desc()).limit(50).all()
    return render_template('index.html', entries=entries)

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username exists, pick another.')
            return redirect(url_for('main.register'))
        u = User(username=form.username.data, display_name=form.display_name.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Registered. Please login.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    entries = current_user.entries.order_by(Entry.created_at.desc()).all()
    return render_template('dashboard.html', entries=entries)

@bp.route('/entry/add', methods=['GET','POST'])
@login_required
def add_entry():
    form = EntryForm()
    if form.validate_on_submit():
        filename = None
        if 'photo' in request.files and request.files['photo'].filename:
            filename = save_photo(request.files['photo'])
        e = Entry(
            user_id=current_user.id,
            title=form.title.data,
            type=form.type.data,
            notes=form.notes.data,
            photo_filename=filename,
            interest_tags=form.interests.data,
            published=form.published.data
        )
        db.session.add(e)
        db.session.commit()
        flash('Saved!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_entry.html', form=form)

@bp.route('/uploads/<path:key>')
def uploaded_file(key):
    # Handle local stored files (prefixed with local://) or S3 keys
    if key.startswith("local://"):
        fname = key.split("local://",1)[1]
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], fname)

    if current_app.config.get('USE_S3') and current_app.config.get('S3_BUCKET'):
        s3 = boto3.client('s3', region_name=current_app.config.get('S3_REGION'))
        bucket = current_app.config['S3_BUCKET']
        try:
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=900
            )
            return redirect(url)
        except ClientError:
            abort(404)
    abort(404)

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/admin/pending')
@login_required
def admin_pending():
    if not current_user.is_admin():
        abort(403)
    pending = Entry.query.filter_by(publish_requested=True, published=False).all()
    return render_template('admin_pending.html', entries=pending)

@bp.route('/admin/approve/<int:entry_id>', methods=['POST'])
@login_required
def admin_approve(entry_id):
    if not current_user.is_admin():
        abort(403)
    e = Entry.query.get_or_404(entry_id)
    e.published = True
    e.publish_requested = False
    db.session.commit()
    flash("Approved!")
    return redirect(url_for('main.admin_pending'))

@bp.route('/admin/reject/<int:entry_id>', methods=['POST'])
@login_required
def admin_reject(entry_id):
    if not current_user.is_admin():
        abort(403)
    e = Entry.query.get_or_404(entry_id)
    e.publish_requested = False
    db.session.commit()
    flash("Rejected!")
    return redirect(url_for('main.admin_pending'))

