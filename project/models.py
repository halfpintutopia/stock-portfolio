# As the database is not associated with a blueprint,
# the file will be kept outside any blueprints
from werkzeug.security import generate_password_hash, check_password_hash

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


class User(database.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in the this table:
        * email - email address of the user
        * hashed password - hash password (using werkzeug.security)

    REMEMBER: Never store the plaintext password in a database!
    """
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    # Add the unique=True parameter to prevent duplicate emails
    email = database.Column(database.String, unique=True)
    password_hashed = database.Column(database.String(128))

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    # the @staticmethod decorator to indicate that it is a static method
    # within the User class that doesn't rely on any instance variable
    @staticmethod
    # underscore ('_') at the start of the method name is a
    # convention in Python to indicate that the method should be considered private.
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self: email}>'

    # The property decorator is used to create read-only methods for a class,
    # which are often referred to as 'getters' in object-oriented programming
    @property
    def is_authenticated(self):
        """
        Return True if the user has been successfully registered
        """
        return True

    @property
    def is_active(self):
        """
        Always True, as all users are active
        """
        return True

    @property
    def is_anonymous(self):
        """
        Always False, as anonymous users aren't supported
        """
        return False

    def get_id(self):
        """
        Return the user ID as a unicode string (`str`)
        """
        return str(self.id)
