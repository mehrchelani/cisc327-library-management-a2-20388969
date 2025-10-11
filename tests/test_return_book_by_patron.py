# Requirement 4
import pytest
from library_service import (
    return_book_by_patron
)
'''Test to see if a book id and patron id correctly returns a book'''
def test_accept_book_and_patron_id_successful():
    success, message = return_book_by_patron("987654", 1)
    assert success is True

'''Test if a patron can return a book a patron has not borrowed'''
def test_verify_book_was_borrowed_by_patron_reject():
    success, message = return_book_by_patron("987654", 18)
    assert success is False
    assert "book not found" in message.lower()

def test_verify_book_was_borrowed_by_patron_accept():
    success, message = return_book_by_patron("123456", 3)
    assert success is False
    assert "borrowed by patron" in message.lower()

'''Test if the function prints error message if no patron id is entered'''
def test_empty_patron():
    success, message = return_book_by_patron("", 3)
    assert success is False
    assert "patron is required" in message.lower()

'''Test if the return updates the book status'''
def test_if_returns_and_updates():
    success, msg = return_book_by_patron("987654", 8)
    assert success is True
    assert "returned successfully" in msg.lower()

def test_invalid_patron_id():
    success, message = return_book_by_patron("12095", 3)
    assert success is False
    assert "invalid patron id. must be exactly 6 digits." in message.lower()

def test_book_not_found():
    success, message = return_book_by_patron("987654", 67)
    assert success is False
    assert "book not found" in message.lower()

def test_no_record():
    success, message = return_book_by_patron("987654", 10)
    assert success is False