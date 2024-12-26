from loguru import logger

from nvidia_util import NvidiaReader

with NvidiaReader() as reader:
    logger.info(reader.get_driver_version())

    for i in range(reader.device_count):
        logger.info(f"====================Device {i} : {reader.get_device_name(i)}=====================")
        total_memory, free_memory, used_memory = reader.get_device_memory_info(i).items()
        logger.info(f'total memory: {total_memory}')
        logger.info(f'free memory: {free_memory}')
        logger.info(f'used memory: {used_memory}')
        logger.info(reader.get_device_fan_speed(i))
        logger.info('=============================')
        reader.get_device_power(i)
