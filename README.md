# Email Cleanup Script

This script is designed to help automate the process of cleaning up your email inbox by deleting emails based on specified search criteria. It supports working with IMAP email providers like Gmail, Yahoo, and others, and can delete emails from all folders or specified folders.

## Features

- **Search by Criteria**: 
  - Delete emails from specific senders (partial match).
  - Delete emails sent to specific recipients (partial match).
  - Delete emails within specific date ranges.
  - Delete emails containing specific keywords in the body or subject.
  
- **Supports Gmail Special Folders**: The script handles Gmail-specific folders like `[Gmail]/All Mail` and `[Gmail]/Sent Mail`.

- **Logging**: The script provides detailed logs for every operation, including successful deletions and errors.

## Prerequisites

- Python 3.x
- Libraries:
  - `imaplib` (for email communication via IMAP)
  - `email` (to parse email headers and bodies)
  - `logging` (for logging)
  
- **Email account credentials** (username/password or app-specific passwords for services like Gmail).

### Required Libraries

Ensure that you have all the required libraries installed by using `requirements.txt`. You can install the required libraries via pip.

```bash
pip install -r requirements.txt
```

Here’s the content of `requirements.txt`:

```txt
imaplib
email
logging
```

## Configuration

Create a `config.py` file in the same directory as this script. This file should contain the following:

```python
EMAIL_ADDRESS = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password-or-app-password"
IMAP_SERVER = "imap.example.com"  # For Gmail, use "imap.gmail.com"
LOGGING = True  # Set to False to disable logging

SEARCH_CRITERIA = {
    "FROM": "example@example.com",      # Delete emails from this sender
    "TO": "support@example.com",         # Delete emails sent to this recipient
    "SINCE": "01-Jan-2023",              # Delete emails since this date
    "BEFORE": "31-Dec-2023",             # Delete emails before this date
    "BODY": "error",                     # Delete emails with this keyword in the body
    "SUBJECT": "urgent"                  # Delete emails with this keyword in the subject
}

ACTIONS = [
    "FROM",  # Delete emails from the specified sender
    "TO",    # Delete emails sent to the specified recipient
    "SINCE", # Delete emails from the specified date
    "BEFORE",# Delete emails up to the specified date
    "BODY",  # Delete emails containing specific body keywords
    "SUBJECT"# Delete emails containing specific subject keywords
]
```

### Folder Handling for Gmail

The script is designed to handle Gmail-specific folder structures like `[Gmail]/All Mail`, `[Gmail]/Sent Mail`, etc. If you are using Gmail, make sure to use the appropriate folder names. For example:

- For all mail: `[Gmail]/All Mail`
- For sent mail: `[Gmail]/Sent Mail`
  
For other email services, just use the folder names as they are.

## How It Works

### Step 1: **Connect to Email Server**

The script connects to the specified IMAP server using your email credentials.

### Step 2: **Select Folders**

The script will automatically select all folders in your email account. For Gmail, it will also handle Gmail-specific folders correctly.

### Step 3: **Apply Search Criteria**

The script will search for emails based on the criteria you’ve configured in `config.py`. It will search for:

- Emails from specific senders (`FROM`)
- Emails sent to specific recipients (`TO`)
- Emails received within specific date ranges (`SINCE`, `BEFORE`)
- Emails containing specific keywords in the body or subject (`BODY`, `SUBJECT`)

### Step 4: **Delete Emails**

If any emails match the search criteria, they will be marked for deletion and permanently removed after the expunge operation.

### Step 5: **Logging**

Logs are generated for every action, including successful email deletions and errors.

## Usage

1. Update the `config.py` file with your email credentials and search criteria.
2. Run the script:

```bash
python email_cleanup.py
```

### Example Output

If the script successfully deletes emails based on the criteria, you will see logs similar to:

```text
2025-01-16 14:40:15,786 - Marked email 12345 for deletion with criteria: FROM "Terabox"
2025-01-16 14:40:16,209 - Marked email 67890 for deletion with criteria: SUBJECT "LeetCode"
2025-01-16 14:40:16,628 - Deleted emails with criteria: FROM "Terabox"
2025-01-16 14:40:17,052 - Deleted emails with criteria: SUBJECT "LeetCode"
```

If no emails are found for the criteria:

```text
2025-01-16 14:40:17,473 - No emails found with criteria: BODY "LeetCode"
```

### Error Handling

If there’s an issue (e.g., connection issues, invalid credentials, or search failures), the script will log the error and exit gracefully.

```text
2025-01-16 14:40:15,786 - Error searching or deleting emails in folder "[Gmail]" with criteria FROM "Terabox": command SEARCH illegal in state AUTH, only allowed in states SELECTED
```

## Notes

- Make sure to use an **app-specific password** if using Gmail or other providers that require this for enhanced security.
- You can modify the search criteria and actions in `config.py` to fit your needs.
- The script will process each search criterion one by one, so emails may be deleted separately for each search criterion.
  
## Troubleshooting

1. **Invalid Credentials**: Ensure you're using the correct email credentials and app-specific password if required.
2. **Gmail Folder Issues**: Ensure that you are using the correct folder names, especially for Gmail.