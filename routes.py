from flask import render_template, url_for, flash, redirect, request
from main import app, db, bcrypt
from models import User, Job
from forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from utils import log_event, get_exchange_rates
import logging
import os
import secrets
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    rates = get_exchange_rates()

    if search:
        jobs = Job.query.filter(Job.title.ilike(f'%{search}%')) \
            .order_by(Job.date_posted.desc()) \
            .paginate(page=page, per_page=5)
    else:
        jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', jobs=jobs, rates=rates, search=search)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('თქვენ წარმატებულად დარეგისტრირდით!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            logging.info(f"წარმატებული ავტორიზაცია: {user.email}")
            return redirect(url_for('home'))
        else:
            logging.warning(f"წარუმატებელი ავტორიზაცია: {form.email.data}")
            flash("თქვენ ვერ შეხვედით თქვენს ანგარიშზე.", "danger")
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("თქვენ გამოხვედით სისტემიდან", "info")
    return redirect(url_for('home'))

@app.route('/job/create', methods=['GET', 'POST'])
@login_required
def post_job():
    form = PostForm()
    if request.method == 'POST':
        print(f"მონაცემები წამოვიდა: {request.form}")

    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            description=form.content.data,
            company=form.company.data,
            location=form.location.data,
            category=form.category.data,
            salary=form.salary.data,
            author=current_user
        )
        db.session.add(job)
        db.session.commit()
        flash("ვაკანსია წარმატებით გამოქვეყნდა!", "success")
        logging.info(f"დაემატა ვაკანსია: {job.title} მომხმარებლის მიერ: {current_user.email}")
        return redirect(url_for('home'))
    if form.errors:
        print(f"ვალიდაციის შეცდომები: {form.errors}")
    return render_template('create.html', title='ახალი ვაკანსია', form=form)

@app.route("/job/<int:job_id>")
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', title=job.title, job=job)

@app.route("/job/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        flash("თქვენ არ გაქვთ ამის უფლება!", "danger")
        return redirect(url_for('home'))

    db.session.delete(job)
    db.session.commit()
    flash("ვაკანსია წარმატებით წაიშალა!", "success")
    return redirect(url_for('home'))


@app.route("/job/<int:job_id>/update", methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        flash("თქვენ არ გაქვთ ამ ვაკანსიის რედაქტირების უფლება!", "danger")
        return redirect(url_for('home'))

    form = PostForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.description = form.content.data
        job.company = form.company.data
        job.location = form.location.data
        job.category = form.category.data
        job.salary = form.salary.data
        db.session.commit()
        flash('ვაკანსია განახლდა!', 'success')
        return redirect(url_for('job_detail', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.content.data = job.description
        form.company.data = job.company
        form.location.data = job.location
        form.category.data = job.category
        form.salary.data = job.salary

    return render_template('create.html', title='რედაქტირება', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('მონაცემები განახლდა!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = current_user.image_file if current_user.image_file else 'default.jpg'
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route("/user/<string:username>")
def user_jobs(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Job.query.filter_by(user_id=user.id)\
        .order_by(Job.date_posted.desc())\
        .all()
    return render_template('user_jobs.html', jobs=jobs, user=user)

def save_picture(form_picture):
    if current_user.image_file and not current_user.image_file.startswith('http'):
        picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
        os.remove(picture_path)
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500