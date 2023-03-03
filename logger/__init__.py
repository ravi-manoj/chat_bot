import logging.handlers
import logging
import logging,logging.handlers
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename=os.getenv('LOG_PATH'), level=logging.DEBUG, format='%(asctime)-15s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

