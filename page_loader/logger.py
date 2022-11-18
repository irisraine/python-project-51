import logging
import sys

RECORD_FILE_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
RECORD_CLI_FORMAT = "%(levelname)s: %(message)s"
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"


def init_logger(is_logfile=False):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    cli_record_format = logging.Formatter(
        fmt=RECORD_CLI_FORMAT,
        datefmt=DATE_FORMAT
    )
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setFormatter(cli_record_format)
    info_handler.addFilter(lambda record: record.levelno == logging.INFO)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setFormatter(cli_record_format)
    error_handler.addFilter(lambda record: record.levelno >= logging.ERROR)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    if is_logfile:
        file_record_format = logging.Formatter(
            fmt=RECORD_FILE_FORMAT,
            datefmt=DATE_FORMAT
        )
        file_handler = logging.FileHandler(filename="page_loader.log")
        file_handler.setFormatter(file_record_format)
        logger.addHandler(file_handler)

