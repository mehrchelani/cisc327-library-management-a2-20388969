# Requirement 3
import pytest
from library_service import (
    borrow_book_by_patron
)
'''Tests that a valid patron ID and valid book ID can be entered successfully and allows for borrowing'''
def test_valid_borrow_success():
    success, message = borrow_book_by_patron("123456", 2)
    assert success is True
    assert "successfully borrowed" in message.lower()

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

''' Test to check that a book cannot be borrowed if it is not avaliable'''
def test_check_book_availablity(): 
    success, message = borrow_book_by_patron("123456", 3)
    assert success is False
    assert message == "You have reached the maximum borrowing limit of 5 books."

'''Test that a patron cannot borrow more than 5 books'''
def test_patron_borrowing_limits():
    success, message = borrow_book_by_patron("123456", 5)
    assert success is False
    assert message == "You have reached the maximum borrowing limit of 5 books."

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