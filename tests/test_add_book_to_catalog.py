# Requirement 1
import pytest
from library_service import (
    add_book_to_catalog
)

'''Test if title exceeds over 200 characters'''
def test_title_over_200_chars():
    title = "a" * 201
    success, message = add_book_to_catalog(title, "Test Author", "1234567890123",5)
    assert success is False
    assert "title must be less than 200 characters" in message.lower()

'''Test to reject empty title'''
def test_empty_title():
    title = ""
    success, message = add_book_to_catalog(title, "Test Author", "1234567890123",5)
    assert success is False
    assert "title is required" in message.lower()

'''Test valid input that should pass'''
def test_valid_input():
    success, message = add_book_to_catalog("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 3)
    assert success == True
    assert "successfully added" in message

'''Test to see if aithor exceeds 100 characters'''
def test_author_over_100_chars():
    author = "a" * 101
    success, message = add_book_to_catalog("Test Book", author, "1234567890123",5)
    assert success is False
    assert "author must be less than 100 characters" in message.lower()

'''Test to reject empty author'''
def test_empty_author():
    author = ""
    success, message = add_book_to_catalog("Test Book", author, "1234567890123",5)
    assert success is False
    assert "author is required" in message.lower()

'''If ISBN is less than 13 characters, it should be rejected'''
def test_isbn_under_13_chars():
    isbn = "1" * 12
    success, message = add_book_to_catalog("Test Book", "Test Author", isbn ,5)
    assert success is False
    assert "isbn must be exactly 13 digits" in message.lower()

'''If ISBN is greater than 13 characters, it should be rejected'''
def test_isbn_over_13_chars():
    isbn = "1" * 14
    success, message = add_book_to_catalog("Test Book", "Test Author", isbn, 5)
    assert success is False
    assert "isbn must be exactly 13 digits" in message.lower()

'''If ISBN is exactly 13 characters, it passes'''
def test_isbn_exactly_13_passes():
    success,message = add_book_to_catalog("Test Book", "Test Author", "0129384757628", 10)
    assert success is True
    assert "isbn must be exactly 13 digits" in message.lower()

'''Negative total copies should be rejected'''
def test_negative_copies():
    copies = -1
    success, message = add_book_to_catalog("Test Book", "Test Author","1234567890123", copies)
    assert success is False
    assert "total copies must be a positive integer" in message.lower()
    