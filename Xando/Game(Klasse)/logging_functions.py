import logging

log = logging.getLogger(__name__)

# Level: DEBUG, INFO, WARNING, ERROR, CRITICAL
# And i can logs Exceptions

def start_logging(level):
    level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(filename=r'.\logs\game.log', level=level)
    log.info("Logging started")
