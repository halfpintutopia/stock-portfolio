Table of content
- [Tests](#tests)
  - [Structure of tests](#structure-of-tests)
- [Pycharm](#pycharm)
- [Bugs / Errors](#bugs--errors)
  - [Module not found](#module-not-found)

Activate virtual environment

`source venv/bin/activate`

Deactivate virtual environment

`deactivate`

Specify where Flask app is defined

`export FLASK_APP=app.py`

Configure the Flask development server run in «development» mode

`export FLASK_ENV=development`

`export FLASK_DEBUG=1`

`flask run` or `flask --app app --debug run`

# Tests

Run test<br/>
`python -m pytest`

<br>

`python -m pytest -v`

<br>

`python -m pytest --setup-show --cov=project`

or run `pytest` in the interpreter

`tests` directory on the same level as app

test files must either start or end with test (e.g. `_test` or `test_`)

Each folder within the `tests` directory must contain an `__init__.py` file so that the Python interpreter sees it.

## Structure of tests

The Given, When, Then (`Given-When-Then`) structure:

* GIVEN - what are the initial conditions for the test?
* WHEN - what is occurring that needs to be tested?
* THEN - what is the expected response?

GET <br/>
* set response by calling the route e.g. (`response = client.get('/add_stock')`)
* check if status code is 200
* check html string in data response (e.g. `assert b'Stock Symbol <em>(required)</em>' in response.data` )

POST <br/>
* set response by calling the route in the first parameter e.g. (`response = client.post('/add_stock')`)
  * add what needs to be posted to get the response in the second (data required) and third (if redirect) parameters e.g. (`data={'stock_symbol': 'AAPL',
                                     'number_of_shares': '23',
                                     'purchase_price': '432.17'},
                               follow_redirects=True`)
* check if status code is 200


# Pycharm

Settings -> Languages & Frameworks -> Django -> enable support


# Bugs / Errors

## Module not found

After upgrading to Ubuntu 22.04, the update caused the removal of python modules. Had to reinstall.

This is for python3 which comes with Ubuntu.

`sudo apt install python3.10-venv`

`python3 -m venv venv`

`source venv/bin/activate`

Then in virtual environment:

`python --version`

As I already was running a project and had a requirements.txt file

`pip install -r requirements.txt`