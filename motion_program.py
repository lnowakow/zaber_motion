import ZaberLSMDevice as z

import numpy as np
import time
import matplotlib.pyplot as plt
from scipy import signal

def current_milli_time():
    return round(time.time() * 1000)

def main():
    # Create a device object
    LSM = z.ZaberLSMDevice()

    # Home the device
    # if LSM.get_position() != 0:
    #     LSM.home()

    # Move to 25 mm

    LSM.move_absolute(25)
    START_POSITION = LSM.get_position()

    # Define a trajectory
    START_TIME = 0
    END_TIME = 6
    SAMPLE_RATE = 1000
    SAMPLE_PERIOD = 1/SAMPLE_RATE
    T = 0.8
    omega = 2*np.pi/T

    # Sine wave trajectory
    t_traj = np.arange(START_TIME, END_TIME, SAMPLE_PERIOD)
    p_des = np.sin(omega*t_traj) + np.sin(omega*t_traj/2 + 2)
    p_des = p_des - p_des[0]
    dp_des = np.gradient(p_des, SAMPLE_PERIOD)
    max_v = np.max(np.abs(dp_des))
    if max_v > LSM.ABS_MAX_SPEED:
        p_des = p_des* LSM.ABS_MAX_SPEED / max_v
        dp_des = np.gradient(p_des, SAMPLE_PERIOD)
    p_des = START_POSITION + p_des
    l_traj = len(dp_des)

    # Step Input
    # p_des = 5*signal.square(omega*t_traj) + START_POSITION
    # dp_des = np.zeros(len(t_traj))

    # PID control
    Kp = 1
    Ki = 0
    Kd = 0

    # Run the loop
    start = current_milli_time() # start time in milliseconds
    p = [LSM.get_position()]
    t = [0]
    u = [0]
    while (current_milli_time() - start) < END_TIME*1000:
        # Get current time in milliseconds
        t.append(current_milli_time() - start) # index of trajectory

        # Get current position
        p.append(LSM.get_position())

        u.append(dp_des[t[-1] % l_traj] + 
                Kp * (p_des[t[-1] % l_traj] - p[-1]) + 
                Ki * (1) + 
                Kd * (dp_des[t[-1] % l_traj] - (p[-1] - p[-2]) / SAMPLE_PERIOD))


        print(f't: {t[-1]}, p: {p[-1]}, u: {u[-1]}', end='\r')
        
        LSM.move_velocity(u[-1])

    LSM.stop()
    print('\n')

    t = np.asarray(t)/1000 # convert to seconds
    p = np.asarray(p) # convert to numpy array

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(t, p, label="Position")
    ax[0].plot(t_traj, p_des, label="Desired Position")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Position (mm)")
    ax[0].legend()

    ax[1].plot(t, u, label="Control Input")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Velocity (mm/s)")
    ax[1].legend()
    plt.show()

if __name__ == "__main__":
    main()