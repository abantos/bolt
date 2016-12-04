import logging

def initialize_logging(log_level, log_file=None, logger=None):
    logger = logger or logging.getLogger()
    logger.setLevel(log_level)
    # Console logging
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # File logging if specified.
    if log_file:
        handler = logging.FileHandler(log_file, 'w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)