from app import app, forms, db, models
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def home():
	post = forms.Post()
	if post.validate_on_submit():
		post_to_create = models.Posts(content=post.content.data,
		                              author=current_user.id,
		                              time=datetime.now().strftime('%Y%m%d%H%M%S')
		                              )
		db.session.add(post_to_create)
		db.session.commit()
		flash('Post Created Successfully!', category='success')
	return render_template('home.html', post=post, count = count)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = forms.Login()
	if form.validate_on_submit():
		yesorno = None
		for x in list(request.form.getlist('remember')):
			if x == 'on':
				yesorno = True
			else:
				yesorno = False
		attempted_user = models.Users.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
			login_user(attempted_user, remember=yesorno)
			flash("Login Successful!", category='success')
			return redirect(url_for('home'))
		if not attempted_user:
			flash('User Doesn''t exist.', category='danger')
		else:
			flash('Please check your Username and Password', category='warning')

	return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = forms.Register()
	if form.validate_on_submit():
		create_user = models.Users(first_name=form.first_name.data,
		                           last_name=form.last_name.data,
		                           username=form.username.data,
		                           email=form.email.data,
		                           passwordgen=form.password.data
		                           )
		db.session.add(create_user)
		db.session.commit()
		attempted_user = models.Users.query.filter_by(username=form.username.data).first()
		login_user(attempted_user, remember=True)
		flash("Welcome to The Family!. You are now Logged in.", category='success')
		return redirect(url_for('home'))

	if form.errors != {}:
		for error in form.errors.values():
			flash(error, category="danger")
	return render_template('register.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	flash('You Logged out Successfully', category='info')
	return redirect(url_for('home'))


@app.route('/<user>')
def user(user):
	query = models.Users.query.filter_by(username=user).all()
	title = None
	userdata = {}

	if query != []:
		for x in query:
			userdata.update(firstname=x.first_name)
			userdata.update(lastname=x.last_name)
			userdata.update(username=x.username)
			userdata.update(email=x.email)
			userdata.update(friends=x.friends)
			userdata.update(propic=x.propic)
			title = x.first_name + ' ' + x.last_name
		template = 'user.html'
	else:
		template = '404.html'

	return render_template(template, userdata=userdata, title=title)
