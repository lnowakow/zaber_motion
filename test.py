from zaber_motion.binary import Connection, CommandCode
from zaber_motion import Units
import time
import numpy as np

class ZaberDevice:
    def __init__ (port: str = "/dev/ttyUSB0"):
        self.port = port
        self.connection = None
        self.device = None

        setup()

    def setup(self):
        if "/dev/ttyUSB" not in self.port:
            raise ValueError("Invalid port. Must be of the form /dev/ttyUSBx where x is a number.")
        
        # Open the connection.
        self.connection = Connection.open_serial_port(self.port)
        device_list = connection.detect_devices()
        print("Detected {} devices".format(len(device_list)))
        self.device = device_list[0]

        # set minimum and maximum positions
        self.device.set_limit_min(0)
        self.device.set_limit_max(100)



with Connection.open_serial_port("/dev/ttyUSB0") as connection:
    # device_list = connection.detect_devices()
    # print("Detected {} devices".format(len(device_list)))
    # device = device_list[0]
    # device.home()
    # # get device number
    # print(device.get_device_number())
    devices = connection.detect_devices()
    print("Detected {} devices".format(len(devices)))
    device = devices[0]

    # print out device info
    print(f"Device ID: {device.device_id}")
    print(f"Device Type: {device.device_type}")
    print(f"Device Name: {device.name}")
    print(f"Device Identity: {device.identity}")
    print(f"Device Firmware Version: {device.firmware_version}")
    print(f"Device Serial Number: {device.serial_number}")
    print(f"Device Settings: {device.settings}")

    # Set Home and Target Speed
    device.generic_command_with_units(CommandCode.SET_HOME_SPEED, 4, Units.VELOCITY_MILLIMETRES_PER_SECOND)
    device.generic_command_with_units(CommandCode.SET_TARGET_SPEED, 4, Units.VELOCITY_MILLIMETRES_PER_SECOND)

    # # Send home
    # device.generic_command_no_response(CommandCode.HOME)
    # while device.is_busy():
    #     time.sleep(0.1)
    # device.move_absolute(25, Units.LENGTH_MILLIMETRES)
    # while device.is_busy():
    #     time.sleep(0.1)

    # Move with sine wave
    T = 2
    omega = 2*np.pi/T
    start = time.time()
    while (time.time() - start) < 6:
        device.move_velocity(4 * np.sin(omega*time.time()), Units.VELOCITY_MILLIMETRES_PER_SECOND)
        print(f"Current position: {device.get_position(Units.LENGTH_MILLIMETRES)}", end="\r")
        time.sleep(0.01)
    print(f"Current position: {device.get_position(Units.LENGTH_MILLIMETRES)}", end="\r")

    # device.move_velocity(4, Units.VELOCITY_MILLIMETRES_PER_SECOND)
    # start = time.time()
    # while (time.time() - start) < 2:
    #     print(f"Current position: {device.get_position(Units.LENGTH_MILLIMETRES)}", end="\r")
    #     time.sleep(0.01)
    # print(f"Current position: {device.get_position(Units.LENGTH_MILLIMETRES)}")

    # device.move_velocity(-4, Units.VELOCITY_MILLIMETRES_PER_SECOND)
    # start = time.time()
    # while (time.time() - start) < 2:
    #     print(f"Current position: {device.get_position(Units.LENGTH_MILLIMETRES)}", end="\r")
    #     time.sleep(0.01)
    # print(f"Current position: {device.get_position(Units.LENGTH_MILLIMETRES)}")

    device.stop()