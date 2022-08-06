from app import app, forms, db, models
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user


@app.route('/', methods=['GET', 'POST'])
def home():
	post = forms.Post()
	if post.validate_on_submit():
		post_to_create = models.Posts(content = post.content.data,
		                              author = current_user.id
		                              )
		db.session.add(post_to_create)
		db.session.commit()
		flash('Post Created Successfully!', category='success')
	return render_template('home.html', post = post)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = forms.Login()
	if form.validate_on_submit():
		attempted_user = models.Users.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
			login_user(attempted_user)
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
		login_user(attempted_user)
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