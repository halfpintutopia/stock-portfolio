import pytest
from project import create_app
from flask import current_app  # <--- proxy
from project.models import Stock, User
from project import database


@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78')
    return stock


@pytest.fixture(scope='module')
def new_user():
    user = User('siri@email.com', 'privatePassword123')
    return user


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


@pytest.fixture(scope="function")
def register_default_user(test_client):
    # Log in the default user
    test_client.post('/users/register',
                     data={'email': 'siri@email.com',
                           'password': 'privatePassword123'},
                     follow_redirects=True)
    return


@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the default user
    test_client.post('/users/login',
                     data={'email': 'siri@email.com',
                           'password': 'privatePassword123'},
                     follow_redirects=True)
    yield  # this is where the testing happens

    # Log out the default user
    test_client.get('/users/logout', follow_redirects=True)
