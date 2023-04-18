import os
import logging
from flask import Flask, render_template
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler


# ----------------------------
# Application Factory Function
# ----------------------------

# create_app function handles the 'Application State' - create and initialize
def create_app():
    # Creates the Flask application (move from app.py in root to project)
    app = Flask(__name__)

    # Set the configuration variables
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    # Register the blueprints in the project
    register_blueprints(app)
    # Configure the logger
    configure_logging(app)

    register_app_callbacks(app)
    register_error_pages(app)
    return app


def register_blueprints(app):
    from project.stocks import stocks_blueprint
    from project.users import users_blueprint
    # Import blueprints in this function to avoid a circular reference
    # The blueprints effectively handle the 'Steady State' - where requests are processed (by view functions
    # and responses are returned
    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')


def configure_logging(app):
    # Logging Configuration
    file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log',
                                       maxBytes=16384,
                                       backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    # Log that the Flask application is starting
    app.logger.info('Starting the Flask Stock Portfolio App...')


def register_app_callbacks(app):
    @app.before_request
    def app_before_request():
        app.logger.info('Calling before_request() for the Flask application...')

    @app.after_request
    def app_after_request(response):
        app.logger.info('Calling after_request() for the Flask application...')
        return response

    @app.teardown_request
    def app_teardown_request(error=None):
        app.logger.info('Calling teardown_request() for the Flask application...')

    @app.teardown_appcontext
    def app_teardown_appcontext(error=None):
        app.logger.info('Calling teardown_appcontext() for the Flask application...')


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405
