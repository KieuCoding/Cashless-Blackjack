# -*- coding: utf-8 -*-
"""
Peter Kieu, pckieu@.cougarnet.uh.edu, (PSID: 1916075)
"""

import matplotlib.pyplot as plt

filename = 'data.dat'

'''
The read function uses the command open() with r being read mode, to read
the data values inside the provide file "data.dat". After reading the values
, sort the values into a single float list and return that list after
execution. 
'''
def read(filename):
    data_dat = []
    with open(filename, 'r') as data:
        read_line = data.readlines()
        for items in read_line:
            data_dat.append(float(items))
        #print(data_dat)
        return data_dat

'''
The stat function finds the maximum and minimum values in the data list
through a for loop that will store the most Highest and lowest value readings
it can find. Also it will calculate the average by adding up all data value
in one of the for loop, then dividing it to the length of the list.
'''
def stat(data_dat):
    data_dat = read(filename)
    minimum = data_dat[0]
    maximum = data_dat[0]
    length = len(data_dat)
    total = 0 
    for items in data_dat:
        if items < minimum:
            minimum = items
    for items in data_dat:
        if items > maximum:
            maximum = items
        total += items 
    average = total/length
    average, minimum, maximum = float(average), float(minimum), float(maximum)
    return average, minimum, maximum

'''
The count function aquires the user input through the terminal, asking for
how many bins they want to split the list. The number of bins will be divided
under the total length of the list and return the total number of samples per
bin. Using a for loop to store each total samples into each bins, to show
that the data has been split. This function should return the maximum amount
of data samples each bin can hold.
'''
def count(data_dat, num_bins):
    average, minimum, maximum = stat(data_dat)
    data_dat = read(filename)
    bin_range = maximum - minimum
    bin_size = bin_range / num_bins
    bin_count = [0] * num_bins
    
    for items in data_dat:
        bin_ID = (int((items - minimum) / bin_size), num_bins - 1)
        bin_index = min(bin_ID)
        bin_count[bin_index] += 1
     
    return bin_count  
'''
The plot function will need the user input to indicate what range of indexs
they want to see on the plot graph using matplotlib. The plot will use the
matlib commands to label and title the graph, according to the homework, and
will save the plot image as "chart.png" into the working directory that this
main file is using.
'''
def plot(start, end):
    data_dat = read(filename)
    average, minimum, maximum = stat(data_dat)
    range_data = data_dat[start:end]
    
    plt.plot(range_data, label='Selected Data')
    plt.axhline(y=average, color='r', linestyle='--', label='Average')
    plt.axhline(y=minimum, color='g', linestyle='--', label='Minimum')
    plt.axhline(y=maximum, color='b', linestyle='--', label='Maximum')
    
    plt.xlabel('Range of Index')
    plt.ylabel('Data Values')
    plt.title('Users Selected Range of Data')
    plt.legend()
    plt.savefig('chart.png')
    plt.show()
    
'''
plot_count function takes the return list from the count function and sorts
it in ascending order through python's ".sort()" command. Then that sorted
list is plotted on a graph using the matplotlib library.
'''
def plot_count(bin_count):
    bin_count.sort()
    plt.plot(bin_count, marker='o')
    plt.title('Bin Counts in Ascending Order')
    plt.ylabel('Sample Count')
    plt.show()
    
'''
The main function to run the following functions above for homework 2
'''
def main():
    read(filename)
    data_dat = read(filename)
    stat(data_dat)
    num_bins = int(input("please Enter a bin amount: "))
    count(data_dat, num_bins)
    print(f"{count(data_dat, num_bins)}")
    start = int(input("Please enter a starting point: "))
    end = int(input("Please enter an end point: "))
    plot(start, end)
    bin_count = count(data_dat, num_bins)
    plot_count(bin_count)
    
    

if __name__ == '__main__':
    main()        
    