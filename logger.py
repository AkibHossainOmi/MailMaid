import logging
from config import LOGGING

def setup_logging():
    """Set up logging for the script."""
    if LOGGING:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    else:
        logging.disable(logging.CRITICAL)
