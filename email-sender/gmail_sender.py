import base64
from pathlib import Path
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

# Folder where this file is located
BASE_DIR = Path(__file__).resolve().parent

# Absolute paths to credentials and token
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def authenticate():
    """
    Authenticates the user with Gmail and returns the Gmail service.
    """

    print("Starting Gmail authentication...")
    print(f"Credentials path : {CREDENTIALS_FILE}")
    print(f"Token path       : {TOKEN_FILE}")

    print("credentials exists:", CREDENTIALS_FILE.exists())
    print("token exists:", TOKEN_FILE.exists())

    creds = None

    # Load existing token
    if TOKEN_FILE.exists():
        print("Loading existing token...")

        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )

    # Authenticate if needed
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            print("Refreshing expired token...")

            creds.refresh(Request())

        else:

            print("Opening browser for Google login...")

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES
            )

            creds = flow.run_local_server(
                host="localhost",
                port=8080,
                open_browser=True,
                success_message="Authentication successful! You can close this window."
            )

        # Save new token
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

        print("Token saved successfully.")

    print("Creating Gmail service...")

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    print("Gmail service created successfully.")

    return service


def create_message(sender, to, subject, body):
    """
    Creates a Gmail-compatible message.
    """

    message = MIMEText(body)

    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    return {"raw": raw}


def send_email(recipient, subject, body):
    """
    Sends an email through Gmail.
    """

    try:

        print("\n==============================")
        print("Starting email send...")
        print("==============================")

        service = authenticate()

        message = create_message(
            "me",
            recipient,
            subject,
            body
        )

        service.users().messages().send(
            userId="me",
            body=message
        ).execute()

        print(f"\n✅ Email sent successfully to {recipient}")

        return True

    except Exception as e:

        print(f"\n❌ Failed to send email:\n{e}")

        return False