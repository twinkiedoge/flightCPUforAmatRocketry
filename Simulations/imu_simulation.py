#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 12:46:07 2023

@author: zrummler

PURPOSE: Test code for IMU simulation
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append('../Flight Algorithms')
sys.path.append('../Data Generation')

import strapdown as sd
import data_collection as dc

def not_equal(a1, a2, name):
    
    for i, j in zip(a1, a2):
        if i != j:
            print(name, i, j)

# main
if __name__ == "__main__":
    
    dc.reset()
    
    # Import and format data
    print("Running IMU Simulation")
    print("Opening file for truth data...")
    data = pd.read_csv("../Data Generation/traj_raster_30mins_20221115_160156.csv").to_numpy();    
    PVA_truth = data[:, 1:11];
    dt = 0.1

    # Initialize arrays
    print("Initializing arrays...")
    PVA_est = np.zeros((data.shape[0], 10))
    x0 = PVA_truth[0, 0:11];
    x0 = x0[:]; # Force column vector
    PVA_est[0] = x0 # Store initial conditions in first col of estimate

    # Run the strapdown for all data
    print("Running strapdown simulation...")
    for i in range(data.shape[0] - 1): #data.shape[0] - 1
        
        # simulate getting the next IMU reading
        accel, gyro, dt = dc.get_next_imu_reading()
        dV_b_imu = accel * dt
        dTh_b_imu = gyro * dt
        
        # grab our current PVA estimate
        r_ecef = PVA_est[i, 0:3]; # ECEF position [m]
        v_ecef = PVA_est[i, 3:6]; # ECEF velocity [m/s]
        q_e2b = PVA_est[i, 6:10]; # ECEF-to-body Quaternion
    
        # Run an iteration of the strapdown
        r_ecef_new, v_ecef_new, q_e2b_new = sd.strapdown(r_ecef, v_ecef, q_e2b, dV_b_imu, dTh_b_imu, dt);
    
        # Write values back to estimation matrix
        PVA_est[i + 1, 0:3] = r_ecef_new;
        PVA_est[i + 1, 3:6] = v_ecef_new;
        PVA_est[i + 1, 6:10] = q_e2b_new;
    
    print("Plotting results...")
    
    """ this is a terrible way to do this """
    
    ## PLOT POSITION
    plt.figure()
    plt.plot(PVA_truth[:, 0])
    plt.plot(PVA_est[:, 0])
    plt.title("X POSITION")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 1])
    plt.plot(PVA_est[:, 1])
    plt.title("Y POSITION")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 2])
    plt.plot(PVA_est[:, 2])
    plt.title("Z POSITION")
    plt.legend(["Truth","Estimation"])
    
    
    ## PLOT VELOCITY
    plt.figure()
    plt.plot(PVA_truth[:, 3])
    plt.plot(PVA_est[:, 3])
    plt.title("X VELOCITY")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 4])
    plt.plot(PVA_est[:, 4])
    plt.title("Y VELOCITY")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 5])
    plt.plot(PVA_est[:, 5])
    plt.title("Z VELOCITY")
    plt.legend(["Truth","Estimation"])
    
    ## PLOT ATTITUDE
    plt.figure()
    plt.plot(PVA_truth[:, 6])
    plt.plot(PVA_est[:, 6])
    plt.title("SCALAR QUATERNION")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 7])
    plt.plot(PVA_est[:, 7])
    plt.title("I QUATERNION")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 8])
    plt.plot(PVA_est[:, 8])
    plt.title("J QUATERNION")
    plt.legend(["Truth","Estimation"])
    plt.figure()
    plt.plot(PVA_truth[:, 9])
    plt.plot(PVA_est[:, 9])
    plt.title("K QUATERNION")
    plt.legend(["Truth","Estimation"])
    
    dc.reset()