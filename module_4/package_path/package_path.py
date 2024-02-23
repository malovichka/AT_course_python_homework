import importlib.util
from importlib import metadata
import logging
import argparse


VALID_LOG_LEVELS = ["ERROR", "WARNING", "INFO", "DEBUG"]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# creating handler for logging into file
handler_fl = logging.FileHandler("get_package_path.log")
# creating handler for logging into stdout
handler_sl = logging.StreamHandler()
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%m/%d/%Y %I:%M:%S",
    encoding="utf-8",
    handlers=[handler_fl, handler_sl],
)


def logging_options() -> dict:
    """This function is parsing loglevels that are passed as cmd arguments and returns a dictionary where:
    key - logging option: file or stdout
    value - indicated log level
    If args are not passed in cmd, then DEBUG log level will be used by default"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-fl",
        "--filelog",
        action="store",
        choices=VALID_LOG_LEVELS,
        default="DEBUG",
        help="please select logging level for file: ERROR, WARNING, INFO, DEBUG",
    )
    parser.add_argument(
        "-sl",
        "--stdoutlog",
        action="store",
        choices=VALID_LOG_LEVELS,
        default="DEBUG",
        help="please select logging level for console output: ERROR, WARNING, INFO, DEBUG",
    )
    args = parser.parse_args()
    return vars(args)


def set_log_level(logging_option: str, handler: logging.StreamHandler):
    """This function is called to set logging level for each handler
    Args:
    logging_option - file or stdout
    handler - handler that will write logs"""
    arg_log_level = logging_options().get(logging_option)
    # converting string log level value to constant
    numeric_level = logging.getLevelName(arg_log_level)
    handler.setLevel(numeric_level)


def get_package_path(package_name):
    # setting log levels for each handler
    set_log_level("filelog", handler_fl)
    set_log_level("stdoutlog", handler_sl)

    # getting spec for package
    spec = importlib.util.find_spec(package_name)

    if not spec:
        logger.error("Package not found")
        return None

    # splitting into list and then joining back without last element if it's __init__.py in order to return path to folder with package
    package_path = spec.origin.split("\\")
    if package_path[-1] == "__init__.py":
        package_path.pop()
    logger.info("\\".join(package_path))

    # getting json with package metadata
    package_metadata = metadata.metadata(package_name)
    logger.warning(package_metadata["summary"])
    logger.debug(package_metadata["version"])
