"""Tests for EmailService.send_contact_notification."""

from unittest.mock import patch

import pytest
from django.test import override_settings

from base_feature_app.services.email_service import EmailService


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL='noreply@example.com',
    CONTACT_NOTIFICATION_EMAIL='admin@example.com',
)
def test_send_contact_notification_returns_true_on_success():
    """Successful call returns True."""
    with patch('base_feature_app.services.email_service.send_mail') as mock_send:
        mock_send.return_value = 1
        result = EmailService.send_contact_notification(
            name='Juan Pérez',
            email='juan@example.com',
            phone='+57 300 1234567',
            program='Inglés',
        )

    assert result is True
    mock_send.assert_called_once()


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL='noreply@example.com',
    CONTACT_NOTIFICATION_EMAIL='admin@example.com',
)
def test_send_contact_notification_passes_correct_arguments():
    """send_mail receives correct subject, from, recipients, and fail_silently."""
    with patch('base_feature_app.services.email_service.send_mail') as mock_send:
        EmailService.send_contact_notification(
            name='Juan Pérez',
            email='juan@example.com',
            phone='+57 300 1234567',
            program='Inglés',
        )

    args, kwargs = mock_send.call_args
    subject, _message, from_email, recipients = args
    assert 'Inglés' in subject
    assert from_email == 'noreply@example.com'
    assert recipients == ['admin@example.com']
    assert kwargs.get('fail_silently') is False


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL='noreply@example.com',
    CONTACT_NOTIFICATION_EMAIL='admin@example.com',
)
def test_send_contact_notification_subject_contains_program():
    """Email subject line includes the requested program name."""
    with patch('base_feature_app.services.email_service.send_mail') as mock_send:
        EmailService.send_contact_notification(
            name='Ana',
            email='ana@example.com',
            phone='123',
            program='Administración',
        )

    subject = mock_send.call_args[0][0]
    assert 'Administración' in subject


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL='fallback@example.com',
    CONTACT_NOTIFICATION_EMAIL='custom-recipient@example.com',
)
def test_send_contact_notification_uses_contact_notification_email_setting():
    """Recipient is read from CONTACT_NOTIFICATION_EMAIL setting."""
    with patch('base_feature_app.services.email_service.send_mail') as mock_send:
        EmailService.send_contact_notification(
            name='Test',
            email='t@example.com',
            phone='0',
            program='Test',
        )

    recipients = mock_send.call_args[0][3]
    assert recipients == ['custom-recipient@example.com']


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL='noreply@example.com',
    CONTACT_NOTIFICATION_EMAIL='admin@example.com',
)
def test_send_contact_notification_propagates_send_mail_exception():
    """Exception from send_mail propagates to caller."""
    with patch(
        'base_feature_app.services.email_service.send_mail',
        side_effect=Exception('SMTP connection refused'),
    ):
        with pytest.raises(Exception, match='SMTP connection refused') as exc_info:
            EmailService.send_contact_notification(
                name='Err',
                email='err@example.com',
                phone='0',
                program='Test',
            )
    assert 'SMTP connection refused' in str(exc_info.value)


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL='noreply@example.com',
    CONTACT_NOTIFICATION_EMAIL='admin@example.com',
)
def test_send_contact_notification_message_body_format():
    """Message body contains all four contact fields in expected format."""
    with patch('base_feature_app.services.email_service.send_mail') as mock_send:
        EmailService.send_contact_notification(
            name='María López',
            email='maria@example.com',
            phone='+57 311 9876543',
            program='Contaduría',
        )

    message = mock_send.call_args[0][1]
    assert 'Nombre: María López' in message
    assert 'Correo: maria@example.com' in message
    assert 'Teléfono: +57 311 9876543' in message
    assert 'Programa: Contaduría' in message
