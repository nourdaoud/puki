from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo 
from app.models import User
from app import photos 

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators= [DataRequired()])
	password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_password(self, password):
		
		password = str(password)
		print(password)
		errors = []
		if not any(x.isupper() for x in password):
		    errors.append('Your password needs at least 1 capital.\n')
		if not any(x.islower() for x in password):
		    errors.append('Your password needs at least one lower case\n')
		if not any(x.isdigit() for x in password):
		    errors.append('Your password needs at least one digit\n')
		if (len(password) < 8):
		    errors.append('Your password needs to be at least 8 characters long\n')
		if (len(errors)) > 0:
		    raise ValidationError(" ".join(errors))

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidatorError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please user a different email address.')

class UploadForm(FlaskForm):
	photo = FileField(validators=[FileAllowed(photos, u'Image Only!'), FileRequired(u'File was Empty!')])
	submit = SubmitField(u'Upload')

