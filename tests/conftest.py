import pytest
from project import create_app
from flask import current_app  # <--- proxy
from project.models import Stock
from project import database


@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78')
    return stock


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            # Establish an application context before accessing the logger and database
            flask_app.logger.info('Creating database tables in test_client fixture...')

            # Create the database and the database table(s)
            database.create_all()

        yield testing_client  # This is where the testing happens!

        # After the test functions complete, control is returned to the fixture
        # so that the database can be cleared
        with flask_app.app_context():
            database.drop_all()
