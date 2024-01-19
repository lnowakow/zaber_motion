from zaber_motion.binary import Connection, CommandCode
from zaber_motion import Units
import time
import numpy as np


class ZaberLSMDevice:
    def __init__ (self, port: str = "/dev/ttyUSB0"):
        self.__port = port
        self.__connection = None
        self.__device = None

        self.ABS_MAX_SPEED = 4 # mm/s

        self.setup()

    def setup(self):
        if "/dev/ttyUSB" not in self.__port:
            raise ValueError("Invalid port. Must be of the form /dev/ttyUSBx where x is a number.")
        
        # Open the connection.
        self.__connection = Connection.open_serial_port(self.__port)
        device_list = self.__connection.detect_devices()
        print("Detected {} devices".format(len(device_list)))
        self.__device = device_list[0]

        # Set Home and Target Speed
        self.__device.generic_command_with_units(CommandCode.SET_HOME_SPEED, 4, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        self.__device.generic_command_with_units(CommandCode.SET_TARGET_SPEED, 4, Units.VELOCITY_MILLIMETRES_PER_SECOND)

    def move_absolute(self, position: float):
        self.__device.move_absolute(position, Units.LENGTH_MILLIMETRES)
        while self.__device.is_busy():
            time.sleep(0.1)
        return self.__device.get_position(Units.LENGTH_MILLIMETRES)
    
    def move_relative(self, position: float):
        self.__device.move_relative(position, Units.LENGTH_MILLIMETRES)
        while self.__device.is_busy():
            time.sleep(0.1)
        return self.__device.get_position(Units.LENGTH_MILLIMETRES)

    def move_velocity(self, velocity: float):
        if abs(velocity) > self.ABS_MAX_SPEED:
            velocity = np.sign(velocity) * self.ABS_MAX_SPEED
            print(f"Absolute velocity: {velocity} exceeds absolute max of {self.ABS_MAX_SPEED} for device. Clamping...")

        return self.__device.move_velocity(velocity, Units.VELOCITY_MILLIMETRES_PER_SECOND)

    def get_position(self):
        return self.__device.get_position(Units.LENGTH_MILLIMETRES)

    def home(self):
        self.__device.generic_command_no_response(CommandCode.HOME)
        while self.__device.is_busy():
            time.sleep(0.1)
        return self.__device.get_position(Units.LENGTH_MILLIMETRES)
    
    def stop(self):
        return self.__device.stop()
    
    def park(self):
        self.__device.park()

    def unpark(self):
        self.__device.unpark()