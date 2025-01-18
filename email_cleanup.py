import imaplib
import email
from email.header import decode_header
import logging
from config import CONFIG

def setup_logging():
    """Set up logging for the script"""
    if CONFIG['LOGGING']:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    else:
        logging.disable(logging.CRITICAL)

def connect_to_email_server():
    """Connect to the email server and log in"""
    try:
        mail = imaplib.IMAP4_SSL(CONFIG['IMAP_SERVER'])
        mail.login(CONFIG['EMAIL_ADDRESS'], CONFIG['EMAIL_PASSWORD'])
        logging.info(f"Successfully logged in to {CONFIG['EMAIL_ADDRESS']} account.")
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

def search_and_apply_actions(mail, criteria, folder):
    """Search for emails based on the criteria in the specified folder and apply actions"""
    try:
        mail.select(folder)  # Select the folder
        status, messages = mail.search(None, criteria)  # Search emails
        if status != "OK":
            logging.error(f"Failed to search emails in folder {folder} with criteria: {criteria}")
            return []

        email_ids = messages[0].split()

        if email_ids:
            for email_id in email_ids:
                if CONFIG['ACTIONS']['delete']:
                    mail.store(email_id, '+FLAGS', '\\Deleted')  # Mark for deletion
                    logging.info(f"Marked email {email_id} for deletion in folder {folder}.")

                if CONFIG['ACTIONS']['archive']:
                    mail.copy(email_id, CONFIG['ARCHIVE_FOLDER'])
                    logging.info(f"Archived email {email_id} to {CONFIG['ARCHIVE_FOLDER']}.")

                if CONFIG['ACTIONS']['mark_as_read']:
                    mail.store(email_id, '+FLAGS', '\\Seen')
                    logging.info(f"Marked email {email_id} as read in folder {folder}.")

            if CONFIG['ACTIONS']['delete']:
                mail.expunge()  # Permanently remove marked emails
                logging.info(f"Deleted emails in folder {folder}.")
        else:
            logging.info(f"No emails found in folder {folder} with criteria: {criteria}")
    except Exception as e:
        logging.error(f"Error processing emails in folder {folder} with criteria {criteria}: {e}")

def process_criteria(mail):
    """Process each search criterion separately and apply actions to matching emails"""
    folders = CONFIG['FOLDERS'] if CONFIG['FOLDERS'] else get_all_folders(mail)
    if not folders:
        return

    for folder in folders:
        logging.info(f"Processing folder: {folder}")

        for key, value in CONFIG['SEARCH_CRITERIA'].items():
            if value:  # Only proceed if the criterion value is not empty
                search_criteria = f"{key.upper()} \"{value}\""
                search_and_apply_actions(mail, search_criteria, folder)

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
