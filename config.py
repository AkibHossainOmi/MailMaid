CONFIG = {
    "EMAIL_PROVIDER": "gmail",
    "EMAIL_ADDRESS": "your_email@gmail.com",
    "EMAIL_PASSWORD": "your_password",
    "IMAP_SERVERS": {
        "gmail": "imap.gmail.com",
        "yahoo": "imap.mail.yahoo.com",
        "outlook": "imap-mail.outlook.com"
    },
    "IMAP_SERVER": "imap.gmail.com",
    "SEARCH_CRITERIA": {
        "FROM": "",  # Delete emails from this sender
        "TO": "",  # Delete emails sent to this recipient
        "SINCE": "",  # Delete emails from this date onwards
        "BEFORE": "",  # Delete emails before this date
        "BODY": "",  # Delete emails containing this text in the body
        "SUBJECT": ""  # Delete emails with this text in the subject
    },
    "ACTIONS": {
        "delete": True,  # Delete matched emails
        "archive": True,  # Archive matched emails
        "mark_as_read": True  # Mark matched emails as read
    },
    "LOGGING": True,
    "FOLDERS": ["INBOX", "Spam"],  # Specify folders to process, leave empty to process all
    "ARCHIVE_FOLDER": "Archive"  # Folder to move archived emails to
}
