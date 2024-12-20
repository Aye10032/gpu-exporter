from loguru import logger

from nvidia_util import NvidiaReader

with NvidiaReader() as reader:
    logger.info(reader.get_driver_version())

    for i in range(reader.device_count):
        logger.info(f"Device {i} : {reader.get_device_name(i)}")
