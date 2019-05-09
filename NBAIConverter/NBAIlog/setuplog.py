import logging
from logging.handlers import TimedRotatingFileHandler

import colorlog
import os


# log file and console info showing format
def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup log file format and output level"""

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    format_str = '%(asctime)s - %(levelname)-8s - %(filename)s - %(lineno)d - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    if os.isatty(2):
        cformat = '%(log_color)s' + format_str
        colors = {'DEBUG': 'reset',
                  'INFO': 'reset',
                  'WARNING': 'bold_yellow',
                  'ERROR': 'bold_red',
                  'CRITICAL': 'bold_red'}
        formatter = colorlog.ColoredFormatter(cformat, date_format, log_colors=colors)
    else:
        formatter = logging.Formatter(format_str, date_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    handler = TimedRotatingFileHandler(log_file, when='W0', backupCount=0)
    handler.suffix = "%Y%m%d"

    formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s', date_format)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logging.getLogger(name)
