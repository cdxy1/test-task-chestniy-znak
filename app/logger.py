import logging


def get_logger():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logs.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


    return logger
