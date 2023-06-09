from urllib.parse import urlparse
from . import users_blueprint
from flask import render_template, flash, abort, request, current_app, redirect, url_for, escape, \
    copy_current_request_context
from .forms import RegistrationForm, LoginForm
from project.models import User
from project import database, mail
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from threading import Thread


# --------------
# Routes
# --------------

@users_blueprint.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', company_name='TestDriven.io')


@users_blueprint.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@users_blueprint.route('/admin')
def admin():
    abort(403)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        # Checks validators and the CSRF token is correct
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                database.session.add(new_user)
                database.session.commit()
                flash(f'Thanks for registering, {new_user.email}!')
                current_app.logger.info(f'Registered new user: {form.email.data}!')

                # The function that runs in the separate thread
                # copy the request and application context
                # to the separate thread using the @copy_current_request_context
                @copy_current_request_context
                def send_email(message):
                    with current_app.app_context():
                        mail.send(message)

                # Send email to the user that they have registered - NEW!!
                msg = Message(subject="Registration - Flask Stock Portfolio App",
                              body="Thanks for registering with the Flask Stock Portfolio App!",
                              recipients=[form.email.data])

                # mail.send(msg)

                # Create a separate thread to handle sending email in an async manner -
                # as a background task -
                # as sending requires communication with GMail SMTP server
                email_thread = Thread(target=send_email, args=[msg])
                email_thread.start()

                return redirect(url_for('users.login'))
            except IntegrityError:
                database.session.rollback()
                flash(f'ERROR! Email ({form.email.data}) already exists.', 'error')
        else:
            flash(f'Error in form data!')

    return render_template('register.html', form=form)


@users_blueprint.route('/hello/<path:message>')
def print_path(message):
    return f'<h1>Path provided: {escape(message)}</h1>'


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('stocks.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password.data):
                # User's credentials have been validated, so log them in
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in, {current_user.email}!')
                current_app.logger.info(f'Logged in user: {current_user.email}')

                # If the next URL is not specified, redirect to the user profile
                if not request.args.get('next'):
                    return redirect(url_for('users.user_profile'))

                # Process the query to determine if the user should be redirected after logging in
                next_url = request.args.get('next')
                # ParseResult(scheme='http', netloc='127.0.0.1:5000', path='/users/login', params='', query='next=%2Fusers%2Fprofile', fragment='')
                if urlparse(next_url).scheme != '' or urlparse(next_url).netloc != '':
                    current_app.logger.info(f'Invalid next path in login request: {next_url}')
                    logout_user()
                    return abort(400)

                current_app.logger.info(f'Redirecting after valid login to: {next_url}')
                return redirect(next_url)

        flash('ERROR! Incorrect login credentials.', 'error')

    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
# This decorator, which comes from Flask-Login, checks to see if a user is logged in.
# If they are then the view is called. If not, the user will be re-directed to the login page
# that was defined in the Application Factory (project/__init__.py)
@login_required
def logout():
    current_app.logger.info(f'Logged out user: {current_user.email}')
    logout_user()
    flash('Goodbye!')
    return redirect(url_for('stocks.index'))


@users_blueprint.route('/profile')
@login_required
def user_profile():
    return render_template('profile.html')
