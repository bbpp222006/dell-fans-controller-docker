import os
import sys
import time
import traceback

from controller.client import FanController
from controller.logger import logger

    
    
if __name__ == '__main__':

    host = os.getenv('HOST')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    temperature = int(os.getenv('TEMPERATURE'))

    if host is None:
        raise RuntimeError('HOST environment variable not set')

    if username is None:
        raise RuntimeError('USERNAME environment variable not set')

    if password is None:
        raise RuntimeError('PASSWORD environment variable not set')

    client = FanController(host=host, username=username, password=password, temperature=temperature)
    
    try:
        while True:
            try:
                client.run()
                time.sleep(5)
            except Exception as err:
                logger.error(f'run controller failed {err}. {traceback.format_exc()}')
                time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        logger.info("Exiting program... setting fan speed to 20%")
        try:
            client.set_fan_speed(20)
        except Exception as e:
            logger.error(f"Failed to set fan speed on exit: {e}")
        sys.exit(0)