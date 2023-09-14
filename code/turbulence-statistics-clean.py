#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Turbulence statistics implementation

This code is an implementation of kmeans (see: https://en.wikipedia.org/wiki/K-means_clustering ). It generates as well multivariate gaussian data, 
using a random gaussian for each of the NumberOfStates gaussian. A gaussian is defined by a random mean and a random covariance matrix, 
sampled from a Wishart distribution.
'''

__author__ = "Samuel Vorlet"
__contact__ = "samuel.vorlet@epfl.ch"
__date__ = "2023/09/13"   ### Date it was created
__status__ = "Finished" ### Production = still being developed. Else: Concluded/Finished.

####################
# Review History   #
####################

# Reviewd by Samuel Vorlet 20230913

####################
# Libraries        #
####################

# Standard imports  ### (Put here built-in libraries - https://docs.python.org/3/library/)
import statistics # version 3.4

# Third party imports ### (Put here third-party libraries e.g. pandas, numpy)
import numpy as np # version 1.0.1
import matplotlib.pyplot as plt  # version 3.5.2
import pandas as pd # version 1.4.2
import scipy  # version 1.11.2
from scipy import stats # version 1.11.2
from scipy.stats import norm # version 1.11.2
import mat73 # version 0.60

####################
# Data importation #
####################
'''
Aim: import data from time-series
'''

# Creating DataFrame from time-series
data_mat = mat73.loadmat('Renner.mat') # Loadint .mat file

df_data = pd.DataFrame(data_mat) # Convert to DataFrame
df_data.columns = ['data'] # Name the column
data = df_data.to_numpy() # Convert to numpy array

# Calculating the number of samples
num_samples = len(df_data)
print('Num_samples = ', num_samples)

# Ploting the data (entire dataset)
plt.plot(data, label = 'raw data',
         color ='k', linewidth = 0.25)
plt.show()

####################
# Stationarity     #
####################
'''
Aim: check that the statistical properties do not change over time (stationary process)

- Mean: $<u>$
- Standard deviation: $\sigma$
- Variance: $\sigma^2$
- Skewness: $S$
- Kurtosis: $K$

The turbulence intensity is calculated as follow: 
$T_i = 100 \cdot \frac{\sigma}{<u>}$
'''

# Defining basic parameters and constants
nu = 15.32e-6 # kinematic viscosity (m2/s)
subdivisions = 20 # number of subdivisions sections
Fs = 8000 # sampling frequency (Hz)
L = 0.067 # integral length scale L (m)
taylor_lambda = 0.0066 # Taylor length scale (m)
inc_bin = 93 # number of bins to be used to divide the velocity increment series

# Calculating and printing mean, standard deviation, variance, skewness and kurtosis
mean = np.mean(data)
stdev = np.std(data)
var = stdev ** 2
skew = scipy.stats.skew(data)
kurt = scipy.stats.kurtosis(data)

print('Mean: ', mean)
print('Standard deviation: ', stdev)
print('Skewness: ', skew)
print('Kurtosis: ', kurt)
print('Variance: ', var)

# Calculating the NaNs in the data
nan_count = df_data['data'].isna().sum()
print('NaNs: ', nan_count)

# Calculating the turbulence intensity:
Ti = 100*stdev/mean
print('Turbulence intensity: ', str(Ti))

# Descriptive statistics

# Defining n as the number of samples / subdivisions
n = int(num_samples/subdivisions)
print('n: ', n)

# Creating DataFrame with statistics
df_stat = df_data.copy() # First column with data

df_stat['rolling_mean'] = df_stat['data'].rolling(n).mean() 
df_stat['rolling_std'] = df_stat['data'].rolling(n).std() 
df_stat['rolling_skew'] = df_stat['data'].rolling(n).skew() 
df_stat['rolling_kurt'] = df_stat['data'].rolling(n).kurt() 
plt.ylabel('Data')
plt.xlabel('Time')

# Plotting the figure with data
plt.plot(df_data['data'], label='Raw Data', 
         color='k', linewidth = 0.25)
plt.title('NaNs: ' + str(nan_count))
plt.legend(loc = 'upper right')
plt.show()

# Plotting the figure with statistics
plt.plot(df_stat['rolling_mean'], label='Rolling Mean', linewidth = 0.5)
plt.plot(df_stat['rolling_std'], label='Rolling Standard deviation', linewidth = 0.5)
plt.plot(df_stat['rolling_skew'], label='Rolling Skewness', linewidth = 0.5)
plt.plot(df_stat['rolling_kurt'], label='Rolling Kurtosis', linewidth = 0.5)
plt.title('Ti = ' + str(round(Ti,2)) + '%')
plt.legend(loc = 'upper right')
plt.ylabel('Data')
plt.xlabel('Time')
plt.show()

###########################
# Probability dens. func. #
###########################
'''
Aim: plot the probability density function (PDF) of the data with the number of bins specified in the function increment_bin. 
It also plots the Gaussian distribution with the same standard deviation and mean value as of the data. In the title, the range 
of the data (the difference between maximum and minimum values of sample data), the skewness, and flatness of the data are printed.
Documentation: https://machinelearningmastery.com/probability-density-estimation/
'''

# Creating DF with Data sorted in ascending order
df_sorted = df_data.copy()
df_sorted = df_sorted.sort_values(by='data', ascending=True)

# Calculating the range:
x_min = min(df_sorted['data'])
x_max = max(df_sorted['data'])
range_data = x_max - x_min

# Plotting the histogramm
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('range = ' + str(round(range_data,2)))
ax.hist(df_sorted, 
        bins = inc_bin, color = 'k')
plt.xlabel('Data')
plt.show()

# Calculating the PDF with SciPy Gaussian KDE
kde = stats.gaussian_kde(df_sorted['data'])

# Plotting the PDF
x = np.linspace(x_min, x_max ,inc_bin*2)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Mean = ' + str(round(mean,2)) + ', Stdev = ' + str(round(stdev,2)))
ax.scatter(x, kde(x), label="Data", 
            marker = 'o', color = 'w', edgecolor='k',)
ax.axvline(mean, 
            color='k', linestyle = '--', linewidth = 0.75, label = 'Mean')
ax.plot(x, norm.pdf(x, mean, stdev), label = 'Gaussian distribution',
         color = 'k', linestyle = '--', linewidth = '0.75')
ax.legend(loc = 'upper right')
ax.set_ylabel('PDF')
ax.set_xlabel('Data')
plt.show()

