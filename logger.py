import logging

# Create a logger and set its minimum severity level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set its minimum severity level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a file handler and set its minimum severity level
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

# Create a formatter and attach it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Attach the handlers to the logger
# logger.addHandler(console_handler)
logger.addHandler(file_handler)
