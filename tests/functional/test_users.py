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
