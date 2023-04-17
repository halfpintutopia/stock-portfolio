from flask import current_app, render_template, request, session, flash, redirect, url_for
from pydantic import BaseModel, validator, ValidationError
from . import stocks_blueprint


# --------------
# Helper Classes
# --------------

class StockModel(BaseModel):
    """Class for parsing new stock data from a form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()


# --------------
# Routes
# --------------

@stocks_blueprint.route('/')
def index():
    current_app.logger.info("Calling the index() function")
    return render_template('index.html')


@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')

        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            # Save the form data to the session object
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            flash(f'Added new stock ({stock_data.stock_symbol})!', 'success')
            current_app.logger.info(f'Added new stock ({request.form["stock_symbol"]})!')

            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            print(e)

    # This instantiation of the blueprint specifies the name of the blueprint ('stocks')
    # and it specifies the location of the template files within the blueprint
    return render_template('add_stock.html')


@stocks_blueprint.route('/stocks/')
def list_stocks():
    return render_template('stocks.html')
