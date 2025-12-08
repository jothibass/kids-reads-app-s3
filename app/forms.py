from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,80)])
    display_name = StringField('Display Name', validators=[Length(0,120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6,128)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    type = SelectField('Type', choices=[('book','Book'),('trip','Trip'),('activity','Activity')])
    notes = TextAreaField('Notes')
    interests = StringField('Interests (comma separated)')
    photo = FileField('Photo', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Images only!')])
    published = BooleanField('Publish now')
    submit = SubmitField('Save')
