from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SearchField, FileField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError
from app import models

class Register(FlaskForm):
	def validate_username(self, username):
		user = models.Users.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError(f"The Username: {username.data} is chosen. Please choose another one.")

	def validate_email(self, email):
		email = models.Users.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError(f"A Tagg account is already associated with this Email.")

	first_name = StringField(validators=[Length(min=3, max=15), DataRequired()])
	last_name = StringField(validators=[Length(min=3, max=15), DataRequired()])
	username = StringField(validators=[Length(min=4,max=30), DataRequired()])
	email = StringField(validators=[Email(), DataRequired()])
	password = PasswordField(validators=[DataRequired()])
	confirm = PasswordField(validators=[EqualTo('password')])
	submit = SubmitField(label='Sign up')


class Login(FlaskForm):
	username = StringField(validators=[DataRequired()])
	password = PasswordField(validators=[DataRequired()])
	submit = SubmitField(label='Log In')

class Post(FlaskForm):
	content = TextAreaField(validators=[DataRequired(), Length(max=30000)])
	post = SubmitField(label='Post')

class Search(FlaskForm):
	searchbox = SearchField(validators=[Length(max= 100)])
	search = SubmitField(label='Search')
class CoverUpdate(FlaskForm):
	cover = FileField(validators=[DataRequired()])
	update = SubmitField(label='Update')

class PhoneUpdate(FlaskForm):
	phone = StringField(validators=[Length(max=16)])
	update = SubmitField(label='Update')