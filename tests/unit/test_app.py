"""
This file contains the unit tests for the app.py file
"""
from app import StockModel
import pytest


def test_validate_stock_data_nominal():
    """
    GIVEN: Using a helper class to validate the form data
    WHEN: valid data is passed in
    THEN: check that the validation is successful
    """
    stock_data = StockModel(
        stock_symbol="SBUX",
        number_of_shares="100",
        purchase_price="45.67"
    )
    assert stock_data.stock_symbol == 'SBUX'
    assert stock_data.number_of_shares == 100
    assert stock_data.purchase_price == 45.67


def test_validate_stock_data_invalid_stock_symbol():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (invalid stock symbol) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            stock_symbol="SBUX123",
            number_of_shares='100',
            purchase_price='45.67'
        )


def test_validate_stock_data_invalid_number_of_shares():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (invalid number of shares) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            stock_symbol="SBUX",
            number_of_shares='100.123547',
            purchase_price='45.67'
        )


def test_validate_stock_data_invalid_purchase_price():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (invalid purchase price) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            stock_symbol="SBUX",
            number_of_shares='100',
            purchase_price='45,67'
        )


def test_validate_stock_data_missing_input():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (missing input) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel()


def test_validate_stock_data_missing_stock_symbol():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (missing stock symbol) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            number_of_shares='100',
            purchase_price='45.67'
        )


def test_validate_stock_data_missing_number_shares():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (missing number of shares) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            stock_symbol="SBUX",
            purchase_price='45.67'
        )


def test_validate_stock_data_missing_purchase_price():
    """
    GIVEN: using a helper class to validate the form data
    WHEN invalid data (missing purchase price) is passed in
    THEN check that the validation raise a ValueError
    """
    with pytest.raises(ValueError):
        StockModel(
            stock_symbol="SBUX",
            number_of_shares='100',
        )
