#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 12:22:46 2023

@author: zrummler


PURPOSE: Library for data collection from hardware sensors


FUNCTIONS:
    get_next_imu_reading()
    gps_is_ready() - bool
    get_next_gps_reading()
    get_next_barometer_reading
    get_first_quaternion()
    
"""

import pandas as pd
import numpy as np

import platform
platform.processor()


'''
IMPORTANT: Set DEVICE variable to DEVICES[1] if running simulation, or DEVICES[0] if running on the actual rocket
'''
DEVICES = ["BEAGLEBONE", "TESTING ON PC"]
DEVICE = DEVICES[1]

if DEVICE == DEVICES[0]:
    '''
    All the code that falls in this if statement is for the real-time flight computer. As we get our sensors working, we will add the data here
    '''
    
    print("Running on the BeagleBone AI")
    

elif DEVICE == DEVICES[1]:
    '''
    All the code that falls below this else statement is for simulation purposes only. Instead of getting data from sensors, the simulation gets data from the datafiles
    '''
    
    # code for simulation on PC
    imu_reading_number = 0
    gps_reading_number = 0
    
    # reading IMU data
    imu_file_data = pd.read_csv("../Data Generation/traj_raster_30mins_20221115_160156.csv").to_numpy();  
    IMU_data = imu_file_data[:, 11:17];
    IMU_t_sec = imu_file_data[:, 0]
        
    # reading GPS data
    gps_file_data = pd.read_csv("../Data Generation/gps_and_barometer_data.csv").to_numpy();
    GPS_data = gps_file_data[:, 1:4]
    GPS_t_sec = gps_file_data[:, 0]
    
    # determine number of data points to read so we don't overflow end of array
    num_points = min(imu_file_data.shape[0], gps_file_data.shape[0])
    

    def get_next_imu_reading(advance=True):
        '''
        gets the next IMU reading 
        
        Arguments:
            - advance: Boolean (optional), if True then data collection advances, if False then on the next call you will get the same data as before
            
        Returns:
            - accel_xyz: 3 x 1 Numpy array
            - gyro_xyz: 3 x 1 Numpy array
            - dt: time step
        '''
        global imu_reading_number
        
        # extract the next acceleration and angular rotation
        accel_xyz = IMU_data[imu_reading_number, 0:3]
        gyro_xyz = IMU_data[imu_reading_number, 3:6]
        
        # time step computation (dt)
        if imu_reading_number == 0:
            dt = IMU_t_sec[1] - IMU_t_sec[0]
        else:
            dt = IMU_t_sec[imu_reading_number] - IMU_t_sec[imu_reading_number-1]
            
        if advance:
            imu_reading_number += 1    
        
        return accel_xyz, gyro_xyz, dt
     

    def gps_is_ready():
        '''
        returns True if the GPS has a new data value to return, or False if not
        for simulation purposes, GPS gets data every 1.0 seconds
        '''
        global gps_reading_number
        
        if np.isnan(GPS_data[gps_reading_number, 0]):
            gps_reading_number += 1
            #print("FALSE")
            return False
        
        #print("TRUE")
        return True
    
    # get_next_gps_reading()
    #
    # returns the next GPS reading (simulation) """
    def get_next_gps_reading(advance=True):        
        '''
        gets the next GPS reading 
        
        Arguments:
            - advance: Boolean (optional), if True then data collection advances, if False then on the next call you will get the same data as before
            
        Returns:
            - reading: 3 x 1 Numpy array [lat, long, atti]
            - dt: time step
        '''
        global gps_reading_number
        
        # read from the GPS    
        reading = GPS_data[gps_reading_number, 0:3]
        
        # time step computation (dt)
        if gps_reading_number == 0:
            dt = GPS_t_sec[10] - GPS_t_sec[0]
        else:
            dt = GPS_t_sec[imu_reading_number] - GPS_t_sec[imu_reading_number-10]
        
        if advance: # only increment counter if desired
            gps_reading_number += 1
       
        return reading, dt
    

    def get_next_barometer_reading():
        '''
        TODO
        '''
        baro = [0, 0, 0]
        return np.array(baro) # TODO
    

    def get_first_quaternion():
        '''
        returns the initial state of the Quaternion
        
        Returns:
            - a 4 x 1 quaternion, in the form [qs, qi, qj, qk]
        '''
        return imu_file_data[0, 7:11]
    

    def reset():
        '''
        resets data collection variables and counters
        
        Returns:
            - a 4 x 1 quaternion, in the form [qs, qi, qj, qk]
        '''
        global imu_reading_number, gps_reading_number
        imu_reading_number = 0
        gps_reading_number = 0
        

    def done():
        '''
        return True if there is no more data to read, False if not
        for simulation only

        '''
        if (imu_reading_number >= num_points) or (gps_reading_number >= num_points):
            return True
        
        return False