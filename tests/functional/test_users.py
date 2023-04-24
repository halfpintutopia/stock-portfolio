def test_get_registration_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/register')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Registration' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with valid data
    THEN check the response is valid and the user is registered
    """
    response = test_client.post('/users/register',
                                data={'email': 'siri@email.com',
                                      'password': 'privatePassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, siri@email.com!' in response.data
    assert b'Flask Stock Portfolio App' in response.data


def test_invalid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with invalid data (missing password)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/users/register',
                                data={'email': 'siri@email.com',
                                      'password': ''},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, siri@email.com!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'[This field is required.]' in response.data


def test_duplicate_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/register' page is posted to (POST) with the email address for existing user
    THEN check an error message is returned to the user
    """
    test_client.post('/users/register',
                     data={'email': 'siri@email.com',
                           'password': 'privatePassword123'},
                     follow_redirects=True)
    response = test_client.post('/users/register',
                                data={'email': 'siri@email.com',
                                      'password': 'privatePassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, siri@email.com!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'ERROR! Email (siri@email.com) already exists' in response.data


# --------------
# Login and Logout
# Test login:
#   - Get login page (GET)
#   - Successful login (POST)
#   - Unsuccessful login (POST)
#   - Attempting to login when already logged in
# Test logout:
#   - Successful logout (GET)
#   - Attempting to use POST to log out ??
#   - Attempting to logout without being logged in ??
# --------------

def test_get_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Login' in response.data


def test_valid_login_and_logout(test_client, register_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/login' page is posted (POST) with valid credentials
    THEN check the response is valid
    """
    response = test_client.post('/users/login',
                                data={'email': 'siri@email.com',
                                      'password': 'privatePassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for logging in, siri@email.com!' in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Please login to access this page.' not in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/logout' page is requested (GET) for a logged in user
    THEN check the response is valid
    """
    response = test_client.get('/users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Goodbye!' in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Please log in to access this page.' not in response.data


def test_invalid_login(test_client, register_default_user):
    """
       GIVEN a Flask application configured for testing
       WHEN the '/users/login' page is posted (POST) with invalid credentials
       THEN check the response is valid
    """
    response = test_client.post('/users/login',
                                data={'email': 'siri@email.com',
                                      'password': 'private123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'ERROR! Incorrect login credentials.' in response.data
    assert b'Flask Stock Portfolio App' in response.data


def test_valid_login_when_logged_in_already(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing and the default user logged in
    WHEN the '/users/login' page is posted to (POST) with the value of credentials for the default user
    THEN check a warning is returned to the user (already logged in)
    """
    response = test_client.post('/users/login',
                                data={'email': 'siri@email.com',
                                      'password': 'privatePassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Already logged in!' in response.data
    assert b'Flask Stock Portfolio App' in response.data


def test_invalid_logout(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/logout' page is posted to (POST)
    THEN check that a 405 error is returned
    """
    response = test_client.post('/users/logout', follow_redirects=True)
    assert response.status_code == 405
    assert b'Goodbye!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Method Not Allowed' in response.data


def test_invalid_logout_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/logout' page is requested (GET) when the user is not logged in
    THEN check that the user is redirected to the loging page
    """
    test_client.get('/users/logout', follow_redirects=True)  # <- double check no logged in users
    response = test_client.get('/users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Goodbye!' not in response.data
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data


# --------------
# Navigation
# When user is logged in:
#   - Load user profile (GET)
# When user is logged out:
#   - Redirect to login page (GET)
# --------------

def test_user_profile_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing and the default user is logged in
    WHEN the '/users/profile' page is requested (GET)
    THEN check that the profile for the current user is displayed
    """
    response = test_client.get('/users/profile')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile' in response.data
    assert b'Email: siri@email.com' in response.data


def test_user_profile_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/profile' page is requested (GET) when the user is NOT logged in
    THEN check that the user is redirected to the login page
    """
    response = test_client.get('/users/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile!' not in response.data
    assert b'Email: siri@email.com' not in response.data
    assert b'Please log in to access this page.' in response.data


# --------------
# Navigation bar
# When user is logged in:
#   - List stocks
#   - Add stock
#   - Profile
#   - Logout
# When user is logged out:
#   - Register
#   - Login
# --------------

def test_navigation_bar_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET) when the user is logged in
    THEN check that the 'List Stocks', 'Add Stock', 'Profile', 'Logout' links are present
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the' in response.data
    assert b'Flask Stock Portfolio App!' in response.data
    assert b'List Stocks' in response.data
    assert b'Add Stock' in response.data
    assert b'Profile' in response.data
    assert b'Logout' in response.data
    assert b'Register' not in response.data
    assert b'Login' not in response.data


def test_navigation_bar_not_logged_in(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET) when the user is not logged in
    THEN check that the 'Register' and 'Login' links are present
    """
    response = test_client.get('/')
    assert b'Flask Stock Portfolio App' in response.data
    assert b'Welcome to the' in response.data
    assert b'Flask Stock Portfolio App!' in response.data
    assert b'Register' in response.data
    assert b'Login' in response.data
    assert b'List Stocks' not in response.data
    assert b'Add Stock' not in response.data
    assert b'Profile' not in response.data
    assert b'Logout' not in response.data


# --------------
# Enhanced login
# - Parse a query with a valid relative path
# - Parse a query with an invalid full path
# --------------

def test_login_with_next_valid_path(test_client, register_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'users/login?next=%2Fusers%2Fprofile' page is posted to (POST) with a valid user login
    THEN check that the user is redirected to the user profile page
    """
    response = test_client.post('users/login?next=%2Fusers%2Fprofile',
                                data={'email': 'siri@email.com',
                                      'password': 'privatePassword123'},
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Flask Stock Portfolio App' in response.data
    assert b'User Profile' in response.data
    assert b'Email: siri@email.com' in response.data

    # Logout user - reset test
    test_client.get('/users/logout', follow_redirects=True)


def test_login_with_next_invalid_path(test_client, register_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'users/login?next=http://www.badsite.com' page is posted to (POST) with a valid user login
    THEN check that a 400 (Bad Request) error is returned
    """
    response = test_client.post('users/login?next=http://www.badsite.com',
                                data={'email': 'siri@email.com',
                                      'password': 'privatePassword123'},
                                follow_redirects=True)
    assert response.status_code == 400
    assert b'User Profile' not in response.data
    assert b'Email: siri@email.com' not in response.data

