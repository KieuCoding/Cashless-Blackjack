#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Peter Kieu, pckieu@.cougarnet.uh.edu, (PSID: 1916075)

from library import Sensor
"""
This function calulates the mean with the given readed values from
the total number of samples
"""
def calculate_mean(sensor_obj, num_samples):
    sum_samples = 0
    i=0
    while i<num_samples:
        sample = sensor_obj.read()
        sum_samples += sample
        i+=1 
    return sum_samples/num_samples

# Implement here the additional functions
"""
std function calls mean function
gets all number of samples from the for loop
sample readings and mean goes through the standard deviation formula
to return the standard deviation from the sample readings 
"""
def calculate_std(sensor_obj, num_samples):
    mean = calculate_mean(sensor_obj, num_samples) 
    DiffSumSqr = 0
    for i in range(num_samples):
        sample = sensor_obj.read()
        DiffSumSqr += (sample - mean) ** 2
        STD = (DiffSumSqr/ num_samples) ** .5
    return STD
"""
we know the max voltage reading is 5v
first iteration checks if the first reading is less than 5v
after the first iteration, it keeps checking for lower values
after reaching all number of samples, function should have the lowest value
"""
def calculate_min(sensor_obj, num_samples):
    min_value = 5
    i = 0
    while i < num_samples:
        sample = sensor_obj.read()
        if sample < min_value:
            min_value = sample
        i += 1
    return min_value
"""
 we know the lowest voltage reading is 0v
 first iteration checks if the first reading is more than 0v
 after the first iteration, it keeps checking for higher values
 after reaching all number of samples, function should have the Highest value
"""
def calculate_max(sensor_obj, num_samples):
    max_value = 0
    i = 0
    while i < num_samples:
        sample = sensor_obj.read()
        if sample > max_value:
            max_value = sample
        i += 1
    return max_value
"""
this function calls the two function "calculate_min and calculate_max"
which gives the lowest and Highest values read, which then
are subtracted to give us the range of the readings 
"""
def calculate_range(sensor_obj, num_samples):
    max_value = calculate_max(sensor_obj, num_samples)
    min_value = calculate_min(sensor_obj, num_samples)
    Range = max_value - min_value
    return Range
"""
This function will plot each reading's value with printed characters.
5 volts having the highest amount of characters (40) printed
and 0 volts having zero characters printed  
"""
def plot(sensor_obj, num_samples):
    i = 0
    while i < num_samples:
        sample = sensor_obj.read()
        if sample == 5:
            print("______________________________________o")
        elif sample < 5 and sample >= 4:
            print("_____________________________o")
        elif sample < 4 and sample >= 3:
            print("___________________o")
        elif sample < 3 and sample >= 2:
            print("____________o")
        elif sample < 2 and sample >= 1:
            print("______o")
        elif sample < 1 and sample >= 0.5:
            print("__o")
        elif sample < 0.5 or sample == 0:
            print("")
        i += 1
    return
"""
This function will count each reading's value and flag them into
certain range of readings. High is values above 0.75V, mid is values
between 0.75v and 0.25v, and low is values below 0.25v
the amount counted will be represented through the charecter "=" 
"""
def count(sensor_obj, num_samples):
    i , high, mid, low = 0, 0, 0, 0
    string = "="
    while i < num_samples:
        sample = sensor_obj.read()
        if sample < 0.25:
            low += 1
        elif sample >= 0.25 and sample < 0.75:
            mid += 1
        elif sample >= 0.75:
            high += 1
        i += 1
    print("counts below 0.25v")
    low_count = string * low
    print(low_count)
    print("counts between 0.25v and 0.75v")
    mid_count = string * mid
    print(mid_count)
    print("counts above 0.75v")
    high_count = string*high
    print(high_count)
    return
    
    
"""
The main function for this homework
"""
def main():
    num_samples = 100
    sensor_obj = Sensor()       # sensor_obj.read() gives us a float value
    # call the first function and print the returned value
    print("mean = ", calculate_mean(sensor_obj, num_samples))
    # call here the additional functions
    print("STD = ", calculate_std(sensor_obj, num_samples))
    print("Minimum = ", calculate_min(sensor_obj, num_samples))
    print("Maximum = ", calculate_max(sensor_obj, num_samples))
    print("Range = ", calculate_range(sensor_obj, num_samples))
    print("")
    # printed text indicates the visualization of the plot function
    print("____________Text plot graph______________")
    plot(sensor_obj, num_samples)
    print("")
    # printed text indicates the visualization of the count function
    print("____________Count Chart__________________")
    count(sensor_obj, num_samples)

if __name__ == '__main__':
    main()
    
