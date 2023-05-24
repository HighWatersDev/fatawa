import logging


def logging_config():
    return {
        'level': logging.INFO,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'handlers': [
            logging.StreamHandler(),
        ]
    }
