# Requirement 7
import pytest
from library_service import (
    get_patron_status_report
)

'''Test to ensure each currently borrowed book has due dates'''
def test_currently_borrowed_books_with_due_dates():
    status_report = get_patron_status_report("987654")
    for book in status_report["currently_borrowed"]:
        assert "title" in book
        assert "due_date" in book

'''Tests that the total late fees is a valid type - float '''
def test_total_late_fees_owed():
    status_report = get_patron_status_report("123456")
    assert isinstance(status_report["total_late_fees_owed"],(float))

'''Tests that the list of books currently borrowed exists'''
def test_number_of_books_currently_borrowed():
    status_report = get_patron_status_report("246810")
    assert isinstance(status_report["currently_borrowed"], list)

'''Tests that the list of books borrowed exists'''
def test_borrowing_history():
    status_report = get_patron_status_report("135791")
    assert isinstance(status_report["borrowing_history"], list)