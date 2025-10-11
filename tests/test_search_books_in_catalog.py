# Requirement 6
import pytest
from library_service import (
    search_books_in_catalog
)

'''Test searching for a book with the exact ISBN'''
def test_search_exact_isbn():
    search = search_books_in_catalog("9780061120084", "isbn")
    assert len(search) == 1 
    assert search[0]["title"] == "To Kill a Mockingbird"

'''Test searching for a case-insensitive book title'''
def test_search_case_insensitive():
    search = search_books_in_catalog("to KILL a MOCKINGBIRD", "title")
    assert len(search) == 1
    assert search[0]["title"]== "To Kill a Mockingbird"

'''Test searching for a book partially'''
def test_search_title_partial():
    search = search_books_in_catalog("gatsby", "title")
    assert len(search) == 1
    assert search[0]["title"] == "The Great Gatsby"
    
'''Test searching for a book author partially'''
def test_search_author_partial():
    search = search_books_in_catalog("scott", "author")
    assert len(search) == 1
    assert search[0]["author"] == "F. Scott Fitzgerald"
