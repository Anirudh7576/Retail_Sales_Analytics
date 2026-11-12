from scripts.common.logger import logger


def test_logger():

    logger.info("Testing INFO message.")

    logger.warning("Testing WARNING message.")

    logger.error("Testing ERROR message.")

    logger.info("Logger test completed.")


if __name__ == "__main__":
    test_logger()