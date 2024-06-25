import logging
import os

def getLogger(componentName: str, logfile: str = None) -> logging.Logger:
    logger = logging.getLogger(componentName)
    if not logger.hasHandlers():  # Prevent adding multiple handlers to the logger
        formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s", datefmt="%H:%M:%S")

        # Determine logs directory
        if logfile:
            logdir = os.path.dirname(logfile)
            # ensure log directory exists
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            file_handler = logging.FileHandler(logfile)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            # if no logfile is provided, log to console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)
        # Don't display info for requests etc.
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger