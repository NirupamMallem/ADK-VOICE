# tools/send_mail.py
import os
from typing import Dict
import smtplib
from email.message import EmailMessage

def capture_details_to_textfile(details: Dict[str, str], filename: str = "details.txt") -> Dict[str, str]:
    """
    Save user-provided details (a dict) to a text file in the current folder.
    Returns a dict with the path written.
    """
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        for k, v in details.items():
            f.write(f"{k}: {v}\n")

    return {"path": path}

def draft_email_from_details(filename: str = "details.txt") -> Dict[str, str]:
    """
    Read the details file and create an email subject and body.
    Returns {"subject": "...", "body": "..."}.
    """
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Details file not found at {path}")

    details = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                k, v = line.split(":", 1)
                details[k.strip()] = v.strip()

    subject = "Your flight booking request"
    if "name" in details:
        subject = f"Flight booking request for {details['name']}"

    lines = []
    lines.append("Hi,")
    lines.append("")
    if "name" in details:
        lines.append(f"This is a booking request for: {details['name']}.")
    if "from" in details and "to" in details:
        lines.append(f"Route: {details['from']} → {details['to']}.")
    if "date" in details:
        lines.append(f"Date: {details['date']}.")
    if "class" in details:
        lines.append(f"Class: {details['class']}.")
    if "notes" in details:
        lines.append("")
        lines.append("Additional notes:")
        lines.append(details["notes"])

    lines.append("")
    lines.append("Please let me know if you need anything else.")
    lines.append("")
    lines.append("Regards,")
    if "name" in details:
        lines.append(details["name"])

    body = "\n".join(lines)

    return {"subject": subject, "body": body}


def _send_via_smtp(user_email: str, subject: str, body: str) -> Dict[str, str]:
    """
    Simple SMTP send. Configure these environment variables in your .env:
      SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM (optional)
    """
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    smtp_from = os.environ.get("SMTP_FROM") or smtp_user

    if not smtp_host or not smtp_user or not smtp_pass:
        raise RuntimeError("SMTP not configured. Set SMTP_HOST, SMTP_USERNAME and SMTP_PASSWORD environment variables.")

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = user_email
    msg["Subject"] = subject
    msg.set_content(body)

    # TLS connection
    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)

    return {"status": "sent_via_smtp", "to": user_email, "subject": subject}


def send_mail(user_email: str) -> Dict:
    """
    Tool to send the drafted email to `user_email`.
    This function:
      1. reads draft from details.txt (in this folder)
      2. sends using SMTP (env vars required)
    Returns a dict with status on success or raises on failure.
    """
    draft = draft_email_from_details()
    subject = draft["subject"]
    body = draft["body"]

    return _send_via_smtp(user_email=user_email, subject=subject, body=body)
