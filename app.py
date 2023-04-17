import logging
from flask import Flask
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
# Import the blueprints
from project.stocks import stocks_blueprint
from project.users import users_blueprint

app = Flask(__name__)

# TEMPORARY
app.secret_key = 'BAD_SECRET_KEY'

# Remove the default logger configured by Flask
app.logger.removeHandler(default_handler)

# Logging Configuration
file_handler = RotatingFileHandler('flask-stock-portfolio.log',
                                   maxBytes=16384,
                                   backupCount=20)
# file_handler = logging.FileHandler('flask-stock-portfolio.log')
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Log that the Flask application is starting
app.logger.info('Starting the Flask Stock Portfolio App...')

# Register blueprints
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')
