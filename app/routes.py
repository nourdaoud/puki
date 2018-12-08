from flask import render_template, flash, redirect, url_for
from app import app, db, photos, logfile 
from app.forms import LoginForm, RegistrationForm, UploadForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from flask import request 
from werkzeug.urls import url_parse
from resizepkg import resize as rsz 
from flask import send_file 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = UploadForm()
	if form.validate_on_submit():
		filename = photos.save(form.photo.data)
		photos_dir = '/Users/noura/puki/uploaded-images/'
		squared_image_loc = rsz.square_image('/Users/noura/puki/uploaded-images/' + filename)
		#squared_image = rsz.square_image(form.photo.data.open())
		#squared_filename = photos.save(squared_image)
		#file_url = photos.url(squared_image)
		#print (file_url)
		squared_image_loc_split = squared_image_loc.split('/')
		squared_image_filename = squared_image_loc_split[len(squared_image_loc_split) - 1]
		print('split result' + squared_image_filename)
		return redirect(url_for('download', filename = squared_image_filename))
	else: 
		file_url = None
	return render_template('index.html', title='Home', form=form,  file_url=file_url)

@app.route("/download_square_photo/<filename>")
def download(filename):
	if (current_user.is_authenticated):
		logfile.debug('user %s attempting to access squared image %s', current_user.username, filename)
	else:
		logfile.debug('Anonymous user is attempting to access squared image %s', filename)
	photos_dir = '/Users/noura/puki/uploaded-images/'
	path = photos_dir + filename 
	try:
		return send_file(path, mimetype='image/png')
	except Exception as e:
		print(e)





@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		logfile.debug('user %s already authenticated', current_user.username)
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			logfile.info('Invalid User or Password.') 
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			logfile.info('%s logged in successfully', user) 
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	if current_user.is_authenticated:
		logfile.info('logging out %s', current_user.username)
	else: 
		logfile.info('anonmyous user attempting to logout')
	logout_user()
	return redirect(url_for('index'))
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		logfile.info('user %s registered successfully.', user)
		flash('Congratulations! You are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)



