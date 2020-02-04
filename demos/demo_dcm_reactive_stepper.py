#!/usr/bin/env python

""" @namespace Demos of the reactive_planners.dcm_reactive_planner.
@file
@copyright Copyright (c) 2017-2019,
           New York University and Max Planck Gesellschaft,
           License BSD-3-Clause
@example
"""

from matplotlib import pyplot as plt
from reactive_planners import DcmReactiveStepper
from py_reactive_planners.lipm_simulator import LipmSimpulator
import numpy as np

if __name__ == "__main__":
    # Create the simulator.
    sim = LipmSimpulator(.2)

    # Create the controller.
    dcm_reactive_stepper = DcmReactiveStepper()
    # controller initialization.
    is_left_leg_in_contact = True
    l_min = -0.5
    l_max = 0.5
    w_min = -0.5
    w_max = 0.5
    t_min = 0.1
    t_max = 0.2
    l_p = 0.1235 * 2
    com_height = 0.26487417
    weight = [1, 1, 5, 100, 100, 100, 100, 100, 100]
    mid_air_foot_height = .05
    control_period = 0.001
    dcm_reactive_stepper.initialize(
        is_left_leg_in_contact, l_min, l_max, w_min, w_max, t_min, t_max,
        l_p, com_height, weight, mid_air_foot_height, control_period)

    # Default parameters.
    u_current_step = np.zeros((3, 1))
    u_current_step[:] = [[.0], [0.1235], [.0]]
    v_des = np.zeros((3, 1))
    x_com = np.zeros((3, 1))
    x_com[:] = [[.0], [.0], [.2]]
    xd_com = np.zeros((3, 1))
    time = 0

    # Plot lists.
    plt_time = []
    plt_x_com = []
    plt_xd_com = []
    plt_right_foot_position = []
    plt_right_foot_velocity = []
    plt_right_foot_acceleration = []
    plt_left_foot_position = []
    plt_left_foot_velocity = []
    plt_left_foot_acceleration = []
    plt_time_from_last_step_touchdown = []
    plt_step_duration = []
    plt_current_support_foot = []

    # Control loop.
    for i in range(1000):
        # update the time
        time += 0.001

        # Compute the next foot location
        dcm_reactive_stepper.run(
            time, dcm_reactive_stepper.get_flying_foot_position(),
            x_com, xd_com, 0.0)
        # simulate a linearized inverted pendulum
        x_com, xd_com, _ = sim.step(
            dcm_reactive_stepper.get_time_from_last_step_touchdown(),
            dcm_reactive_stepper.get_current_support_foot_position().reshape((3, 1)),
            x_com, xd_com)

        # plot collection
        plt_time.append(time)
        plt_x_com.append(x_com.copy())
        plt_xd_com.append(xd_com.copy())
        plt_right_foot_position.append(
            dcm_reactive_stepper.get_right_foot_position())
        plt_right_foot_velocity.append(
            dcm_reactive_stepper.get_right_foot_velocity())
        plt_right_foot_acceleration.append(
            dcm_reactive_stepper.get_right_foot_acceleration())
        plt_left_foot_position.append(
            dcm_reactive_stepper.get_left_foot_position())
        plt_left_foot_velocity.append(
            dcm_reactive_stepper.get_left_foot_velocity())
        plt_left_foot_acceleration.append(
            dcm_reactive_stepper.get_left_foot_acceleration())
        plt_time_from_last_step_touchdown.append(
            dcm_reactive_stepper.get_time_from_last_step_touchdown())
        plt_step_duration.append(
            dcm_reactive_stepper.get_step_duration())
        plt_current_support_foot.append(
            dcm_reactive_stepper.get_current_support_foot_position())

    # Plots.
    plt.figure("com")
    plt.plot(plt_time, np.array(plt_x_com)[:, 0])
    plt.plot(plt_time, np.array(plt_x_com)[:, 1])
    plt.plot(plt_time, np.array(plt_x_com)[:, 2])

    plt.figure("xd")
    plt.plot(plt_time, np.array(plt_xd_com)[:, 0])
    plt.plot(plt_time, np.array(plt_xd_com)[:, 1])
    plt.plot(plt_time, np.array(plt_xd_com)[:, 2])

    plt.figure("right_foot_pos")
    plt.plot(plt_time, np.array(plt_right_foot_position)[:, 0])
    plt.plot(plt_time, np.array(plt_right_foot_position)[:, 1])
    plt.plot(plt_time, np.array(plt_right_foot_position)[:, 2])

    plt.figure("left_foot_pos")
    plt.plot(plt_time, np.array(plt_left_foot_position)[:, 0])
    plt.plot(plt_time, np.array(plt_left_foot_position)[:, 1])
    plt.plot(plt_time, np.array(plt_left_foot_position)[:, 2])

    plt.figure("foot_pos_z")
    plt.plot(plt_time, np.array(plt_right_foot_position)[:, 2])
    plt.plot(plt_time, np.array(plt_left_foot_position)[:, 2])

    plt.figure("last_step_touchdown")
    plt.plot(plt_time, np.array(plt_time_from_last_step_touchdown)[:])
    plt.plot(plt_time, np.array(plt_step_duration)[:])

    plt.figure("support_foot")
    plt.plot(plt_time, np.array(plt_current_support_foot)[:, 0])
    plt.plot(plt_time, np.array(plt_current_support_foot)[:, 1])
    plt.plot(plt_time, np.array(plt_current_support_foot)[:, 2])
    plt.show()
