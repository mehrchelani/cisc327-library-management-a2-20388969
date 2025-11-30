import pytest
from unittest.mock import Mock
from services.library_service import (pay_late_fees, refund_late_fee_payment)
from services.payment_service import PaymentGateway

# pay_late_fees tests
def test_successful_late_fee_payment(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book",  return_value={"fee_amount": 10.0, "days_overdue": 4, "status": "overdue"})
    mocker.patch("services.library_service.get_book_by_id", return_value = {"id": 1, "title": "Test Book"})

def test_refund_invalid_transaction_id_does_not_call_gateway():
    gateway = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("invalid_id", 10.0, gateway)
    assert success is False
    assert message == "Invalid transaction ID."
    gateway.refund_payment.assert_not_called()

def test_invalid_patron_id():
    gateway = Mock(spec=PaymentGateway)
    success, message, id = pay_late_fees("invalid patron", 4, gateway)
    assert success is False
    assert message == "Invalid patron ID. Must be exactly 6 digits."
    assert id is None
    gateway.process_payment.assert_not_called()

def test_zero_late_fees(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0.0, "days_overdue": 0, "status": "no late fee"})
    gateway = Mock(spec=PaymentGateway)
    success, message, txn_id = pay_late_fees("678910", 4, gateway)
    assert success is False
    assert message == "No late fees to pay for this book."
    assert txn_id is None
    gateway.process_payment.assert_not_called()

def test_network_error_handling (mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value = {"fee_amount": 15.0, "days_overdue": 5, "status": "overdue"})
    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 8, "title": "Test Book"})
    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.side_effect = Exception("Network error")
    success, message, txn_id = pay_late_fees("839201", 8, gateway)
    assert success is False
    assert message ==  "Payment processing error: Network error"
    assert txn_id is None
    gateway.process_payment.assert_called_once()

#refund_late_fee_payment tests
def test_successful_refund():
    gateway = Mock(spec=PaymentGateway)
    gateway.refund_payment.return_value = (True, "Refund OK")
    success, message = refund_late_fee_payment("txn_654321", 10.0, gateway)
    assert success is True
    assert "Refund OK" in message
    gateway.refund_payment.assert_called_once_with("txn_654321", 10.0)

def test_invalid_transaction_id():
    gateway = Mock(spec = PaymentGateway)
    success, message= refund_late_fee_payment("badid_654321", 10.0, gateway)
    assert success is False
    assert message == "Invalid transaction ID."
    gateway.refund_payment.assert_not_called()

def test_negative_refund_amount():
    gateway = Mock(spec = PaymentGateway)
    success, message = refund_late_fee_payment("txn_987654", -10.0, gateway)
    assert success is False
    assert message == "Refund amount must be greater than 0."
    gateway.refund_payment.assert_not_called()

def test_zero_refund_amount():
    gateway = Mock(spec = PaymentGateway)
    success, message = refund_late_fee_payment("txn_987654", 0.0, gateway)
    assert success is False
    assert message == "Refund amount must be greater than 0."
    gateway.refund_payment.assert_not_called()

def test_exceeds_fifteen():
    gateway = Mock(spec = PaymentGateway)
    success, message = refund_late_fee_payment("txn_987654", 16.0, gateway)
    assert success is False
    assert message == "Refund amount exceeds maximum late fee."
    gateway.refund_payment.assert_not_called()



                                                                            