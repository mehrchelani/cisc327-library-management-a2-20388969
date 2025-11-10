# Requirement 5
import pytest
from services.library_service import (
    calculate_late_fee_for_book
)
from datetime import datetime, timedelta

@pytest.fixture(autouse=True)
def patch_borrow_records(monkeypatch):
    """Provide fake borrow records for fee tests."""
    now = datetime.now()

    def fake_get_patron_borrowed_books(patron_id: str):
        mapping = {
            
            "098765": [{"patron_id": "098765", "book_id": 1, "due_date": now}], # on time
            "654321": [{"patron_id": "654321", "book_id": 6, " due_date": now - timedelta(days=5)}], # 5 days late
            "864261": [{"patron_id": "864261", "book_id": 9, "due_date": now - timedelta(days=11)}],# 11 days late
            "123456": [{"patron_id": "123456", "book_id": 2, "due_date": now - timedelta(days=20 )}],# 20 days late
        }
        return mapping.get(patron_id, [])

    import services.library_service as library_service
    monkeypatch.setattr(
        library_service, "get_patron_borrowed_books", fake_get_patron_borrowed_books
    )


'''Tests if a book is returned on time, meaning there is no late fee / not overdue'''
def test_no_late_fee():
    charge = calculate_late_fee_for_book("098765", 1)
    assert charge["fee_amount"] == 0.0
    assert charge["days_overdue"] == 0
    assert charge["status"].lower() == "no late fee"

'''Calculates the late fee for a book returned less than 7 days after due date
def test_before_first_seven_days():
    charge = calculate_late_fee_for_book("654321",6)
    assert charge["fee_amount"] == 0.5 * 5
    assert charge["days_overdue"] == 5
    assert charge["status"].lower() == "overdue by 5 days"
    '''

'''Calculates the late fee for a book returned over 7 days after due date'''
def test_after_first_seven_days():
    charge = calculate_late_fee_for_book("864261",9)
    assert charge["fee_amount"] == (0.5 * 7) + (1.0 * 4)
    assert charge["days_overdue"] == 11
    assert charge["status"].lower() == "overdue by 11 days"

'''Tests that the late fees do not exceed the max charge, $15.00'''
def test_max_charge_per_book():
    charge = calculate_late_fee_for_book("123456", 2)
    assert charge["fee_amount"] <= 15.00
    assert charge["days_overdue"] == 20
    assert charge["status"].lower() == "overdue by 20 days"