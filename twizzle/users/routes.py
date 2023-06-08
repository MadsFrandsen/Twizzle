from flask import Blueprint
import os
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from twizzle import bcrypt
from twizzle.queries import insert_user, get_user_by_email, update_user_info, get_some_posts_by_user, get_user_post_count, get_user_by_name, update_user_password, has_user_liked_post, get_likes_for_post
from twizzle.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from twizzle.users.utils import save_picture, send_reset_email
from twizzle.models import User
from flask_login import login_user, current_user, logout_user, login_required



users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = dict(email_address=form.email.data,
                         user_name=form.username.data,
                         password=hashed_password)
        user = User(user_data)
        insert_user(user)
        flash('Your account has been created You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != 'default.jpg':
                picture_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
                os.remove(picture_path)
            current_user.image_file = picture_file
        current_user.user_name = form.username.data
        current_user.email_address = form.email.data
        update_user_info(current_user)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.user_name
        form.email.data = current_user.email_address
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)


@users.route("/user/<string:user_name>")
def user_posts(user_name):
    page = request.args.get('page', 1, type=int)
    user = get_user_by_name(user_name)
    total_posts = get_user_post_count(user)
    limit = 5
    total_pages = (total_posts['count'] + limit) // limit

    if page < 1 or page > total_pages:
        abort(404)

    offset = (page - 1) * limit
    posts = get_some_posts_by_user(user, offset, limit)

    for post in posts:
        likes_count = get_likes_for_post(post['post_id'])
        post['likes'] = likes_count
        if current_user.is_authenticated:
            has_liked = has_user_liked_post(current_user.id, post['post_id'])
            post['liked'] = has_liked

    pages = [i for i in range(1, total_pages+1)]
    return render_template('user_posts.html', posts=posts, user=user, page=page, total_pages=total_pages, pages=pages, total_posts=total_posts['count'])




@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        update_user_password(user)
        flash('Your password has been updated! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)