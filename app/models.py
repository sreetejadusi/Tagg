from app import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
	first_name = db.Column(db.String(length=15), nullable=False)
	last_name = db.Column(db.String(length=15), nullable=False)
	username = db.Column(db.String(length=30), nullable=False, unique=True)
	email = db.Column(db.String(), nullable=False, unique=True)
	password = db.Column(db.String(), nullable=False)
	about = db.Column(db.String())
	friends = db.Column(db.String())
	propic = db.Column(db.String(), default = '../static/propics/profiledef.svg' )
	cover = db.Column(db.String(), default= '../static/coverdef.svg')
	status = db.Column(db.String(), default = 'Yo! I''m Using Tagg!')
	posts = db.relationship('Posts', backref = 'user_posts', lazy= True )
	joined = db.Column(db.String(), nullable= False)
	@property
	def passwordgen(self):
		return self.passwordgen

	@passwordgen.setter
	def passwordgen(self, passwordtemp):
		self.password = bcrypt.generate_password_hash(passwordtemp).decode('utf-8')

	def check_password(self, attempted_password):
		return bcrypt.check_password_hash(self.password, attempted_password)

class Posts(db.Model):
	id = db.Column(db.Integer(), nullable=False, primary_key = True)
	content = db.Column(db.String(length= 30000), nullable= False)
	time = db.Column(db.String())
	author = db.Column(db.Integer(), db.ForeignKey('users.id'))