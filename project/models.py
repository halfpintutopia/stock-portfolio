# As the database is not associated with a blueprint,
# the file will be kept outside any blueprints
from project import database


# All models need to be defined as sub-classes of database.Model
class Stock(database.Model):
    """
    Class that represent a purchased stock in a portfolio

    The following atributes of a stock are stored in this table:
        stock symbols (type: string)
        number of shares (type: integer)
        purchase price (type: integer)

    Note: Due to limitation in the data types supported by SQLite, the
    purchase price is stored as an integer:
        $24.10 -> 2410
        $100.00 -> 1000
        $87.65 -> 8765
    """

    # Sets the name of the table in the database.
    # Singularize the model name (Stock) and pluralize the table name (stocks)
    __tablename__ = 'stocks'

    # The columns of the database are defined as additional class attributes
    id = database.Column(database.Integer, primary_key=True)
    stock_symbol = database.Column(database.String, nullable=False)
    number_of_shares = database.Column(database.Integer, nullable=False)
    purchase_price = database.Column(database.Integer, nullable=False)

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100}'
