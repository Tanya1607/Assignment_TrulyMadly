import logging
import sys

def setup_logging():
    # Create logger
    logger = logging.getLogger("ai_ops_assistant")
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(ch)
    
    return logger

logger = setup_logging()
