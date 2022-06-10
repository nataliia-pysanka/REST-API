import logging.config
import logging
from pathlib import Path

log_path = Path('.').absolute().joinpath("app/util/log.ini")
logging.config.fileConfig(log_path)
logger = logging.getLogger('apiLogger')
