import os
import time
import traceback

from controller.client import FanController
from controller.logger import logger


class PID:
    def __init__(self, kp=1.0, ki=0.1, kd=0.05, setpoint=50.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.last_error = 0.0

    def compute(self, current_value, dt=1.0):
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return output
    
    
if __name__ == '__main__':

    host = os.getenv('HOST')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    temperature = os.getenv('TEMPERATURE')

    if host is None:
        raise RuntimeError('HOST environment variable not set')

    if username is None:
        raise RuntimeError('USERNAME environment variable not set')

    if password is None:
        raise RuntimeError('PASSWORD environment variable not set')

    while True:
        try:
            client = FanController(host=host, username=username, password=password,temperature = temperature)
            client.run()
            time.sleep(5)
        except Exception as err:
            logger.error(
                f'run controller failed {err}. {traceback.format_exc()}'
            )
