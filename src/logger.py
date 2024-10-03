import logging

logging.basicConfig(
    filename='squirrel.log',  # Log output file
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Timestamp format
)

logger = logging.getLogger(__name__)