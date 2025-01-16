EMAIL_PROVIDER = ""
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""

IMAP_SERVERS = {
    "gmail": "imap.gmail.com",
    "yahoo": "imap.mail.yahoo.com",
    "outlook": "imap-mail.outlook.com"
}

IMAP_SERVER = IMAP_SERVERS.get(EMAIL_PROVIDER, "imap.gmail.com")

SEARCH_CRITERIA = {
    "FROM": "",        
    "TO": "",                
    "SINCE": "",  
    "BEFORE": "", 
    "BODY": "",         
    "SUBJECT": ""            
}


ACTIONS = {
    "delete": True, 
    "archive": False,
    "mark_as_read": False
}

LOGGING = True
