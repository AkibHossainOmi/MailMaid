import imaplib
import email
from email.header import decode_header
import logging
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, SEARCH_CRITERIA, ACTIONS, LOGGING

def setup_logging():
    """Set up logging for the script"""
    if LOGGING:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    else:
        logging.disable(logging.CRITICAL)


def connect_to_email_server():
    """Connect to the email server and log in"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        logging.info(f"Successfully logged in to {EMAIL_ADDRESS} account.")
        return mail
    except Exception as e:
        logging.error(f"Failed to connect to server: {e}")
        exit(1)


def get_all_folders(mail):
    """Fetch all available folders"""
    try:
        status, folders = mail.list()
        if status == "OK":
            return [folder.decode().split(' "/" ')[-1] for folder in folders]
        else:
            logging.error("Failed to fetch folders.")
            return []
    except Exception as e:
        logging.error(f"Error fetching folders: {e}")
        return []


def search_and_delete(mail, criteria, folder):
    """Search for emails based on the criteria in the specified folder and delete them"""
    try:
        mail.select(folder)  # Select the folder
        status, messages = mail.search(None, criteria)  # Search emails
        if status != "OK":
            logging.error(f"Failed to search emails in folder {folder} with criteria: {criteria}")
            return []

        email_ids = messages[0].split()

        if email_ids:
            for email_id in email_ids:
                mail.store(email_id, '+FLAGS', '\\Deleted')  # Mark for deletion
                logging.info(f"Marked email {email_id} for deletion in folder {folder} with criteria: {criteria}")

            mail.expunge()  # Permanently remove marked emails
            logging.info(f"Deleted emails in folder {folder} with criteria: {criteria}")
        else:
            logging.info(f"No emails found in folder {folder} with criteria: {criteria}")
    except Exception as e:
        logging.error(f"Error searching or deleting emails in folder {folder} with criteria {criteria}: {e}")


def process_criteria(mail):
    """Process each search criterion separately and delete matching emails from all folders"""
    folders = get_all_folders(mail)  # Get all folders
    if not folders:
        return

    # Process each folder
    for folder in folders:
        logging.info(f"Processing folder: {folder}")
        
        # Step 1: Delete emails from specific sender (Partial match)
        if SEARCH_CRITERIA.get("FROM"):  # Only proceed if 'FROM' is not empty
            search_criteria = f"FROM \"{SEARCH_CRITERIA['FROM']}\""
            search_and_delete(mail, search_criteria, folder)

        # Step 2: Delete emails sent to a specific recipient (Partial match)
        if SEARCH_CRITERIA.get("TO"):  # Only proceed if 'TO' is not empty
            search_criteria = f"TO \"{SEARCH_CRITERIA['TO']}\""
            search_and_delete(mail, search_criteria, folder)

        # Step 3: Delete emails within a specific date range
        if SEARCH_CRITERIA.get("SINCE"):  # Only proceed if 'SINCE' is not empty
            search_criteria = f"SINCE \"{SEARCH_CRITERIA['SINCE']}\""
            search_and_delete(mail, search_criteria, folder)

        if SEARCH_CRITERIA.get("BEFORE"):  # Only proceed if 'BEFORE' is not empty
            search_criteria = f"BEFORE \"{SEARCH_CRITERIA['BEFORE']}\""
            search_and_delete(mail, search_criteria, folder)

        # Step 4: Delete emails with specific keywords in subject or body
        if SEARCH_CRITERIA.get("BODY"):  # Only proceed if 'BODY' is not empty
            search_criteria = f"BODY \"{SEARCH_CRITERIA['BODY']}\""
            search_and_delete(mail, search_criteria, folder)

        if SEARCH_CRITERIA.get("SUBJECT"):  # Only proceed if 'SUBJECT' is not empty
            search_criteria = f"SUBJECT \"{SEARCH_CRITERIA['SUBJECT']}\""
            search_and_delete(mail, search_criteria, folder)


def logout_from_server(mail):
    """Logout from the email server"""
    try:
        mail.logout()
        logging.info("Logged out from the email server.")
    except Exception as e:
        logging.error(f"Error logging out: {e}")


def main():
    """Main function to run the email cleanup automation"""
    setup_logging()
    mail = connect_to_email_server()
    process_criteria(mail)
    logout_from_server(mail)


if __name__ == "__main__":
    main()