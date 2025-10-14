#Requirement 3,
import pytest
from library_service import (
    borrow_book_by_patron,
    add_book_to_catalog
)

'''Test that a patron ID is rejected if it's less than 6 characters'''
def test_patron_id_too_short():
    success, message = borrow_book_by_patron("12345", 2)
    assert success is False
    assert message == "Invalid patron ID. Must be exactly 6 digits."

'''Test that a patron ID is rejected if it's longer than 6 characters'''
def test_accept_book_id_too_long():
    success, message = borrow_book_by_patron("1234567", 2)
    assert success is False
    assert message == "Invalid patron ID. Must be exactly 6 digits."

'''Tests that borrowing fails if patron ID is left blank'''
def test_empty_patron_id():
    success, message = borrow_book_by_patron("", 55)
    assert success is False
    assert message == "Invalid patron ID. Must be exactly 6 digits."

'''Tests that borrowing fails if book ID is left blank'''
def test_empty_book_id():
    success, message = borrow_book_by_patron("123456", None)
    assert success is False
    assert message == "Book not found."