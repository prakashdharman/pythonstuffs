import logging
from logging.handlers import TimedRotatingFileHandler

# Configure the root logger
logging.basicConfig(level=logging.DEBUG)

# Create a timed rotating file handler
handler = TimedRotatingFileHandler('example.log', when='midnight', interval=1, backupCount=3)

# Configure the handler's formatting
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger().addHandler(handler)

# Test the logger
for i in range(10):
    logging.debug(f"Log message {i}")

example.log
example.log-date1
example.log-date2


