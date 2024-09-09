import logging


# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

#handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
