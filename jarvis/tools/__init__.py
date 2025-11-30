# tools/__init__.py
from .send_mail import send_mail, capture_details_to_textfile, draft_email_from_details
__all__ = ["send_mail", "capture_details_to_textfile", "draft_email_from_details"]