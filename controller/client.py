import time
from controller.logger import logger
from controller.ipmi import IpmiTool


class FanController:
    def __init__(self, host: str, username: str, password: str,temperature: int,):
        self.host = host
        self.username = username
        self.password = password
        self.target_temp = temperature

        self.ipmi = IpmiTool(self.host, self.username, self.password)

        # PID 参数（需要你实际调整）
        self.Kp = 3.632
        self.Ki = 0.825
        self.Kd = 1.155


        self.integral = 0.0
        self.last_error = 0.0

    def set_fan_speed(self, speed: int):
        # 限制风扇速度范围在 [10, 100]
        speed = max(1, min(100, speed))
        logger.info(f'Set fan speed: {speed}%')
        self.ipmi.set_fan_speed(speed)

    def pid_control(self, current_temp: float) -> int:
        error = current_temp-self.target_temp

        # 积分
        self.integral += error
        # 防止积分过大
        self.integral = max(-100, min(100, self.integral))

        # 微分
        derivative = error - self.last_error

        # PID 输出
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)

        self.last_error = error

        # 映射到风扇速度
        fan_speed = int(max(1, min(100, output)))
        return fan_speed

    def run(self):
        temperature = max(self.ipmi.temperature())
        logger.info(f'Current maximum temperature: {temperature}')
        if temperature > 70:
            logger.info(f'Switch fan control to auto mode')
            self.ipmi.switch_fan_mode(auto=True)

        speed = self.pid_control(temperature)
        self.set_fan_speed(speed)
