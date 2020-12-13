import sys
print(sys.version)

import numpy as np
import pandas as pd
from ortools.linear_solver import pywraplp
from pulp import *
from mip import Model, xsum, maximize, BINARY
# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
from scipy.optimize import linear_sum_assignment
from scipy.stats import lognorm
import time
from matplotlib import pyplot as plt

df = pd.read_csv("data_duration_large.csv").drop(['Unnamed: 0'], axis=1)

df1 = df[df.duplicated('tpep_pickup_datetime', keep=False)].sort_values('tpep_pickup_datetime').reset_index().drop(["index"], axis=1)

df_instance = df.drop(["trip_duration", "tpep_pickup_datetime", "tpep_dropoff_datetime", \
                       "car_0", "car_1", "car_2", "car_3", "car_4", "car_5", "car_6", \
                       "car_7", "car_8", "car_9"], axis=1)

df_instance = df_instance.iloc[:10000][:]
df_instance.shape

n_cars = 10
deficit = 15
estimated_sigma, loc, scale = lognorm.fit(df_instance['trip_distance'])
estimated_mu = np.log(scale)
l,w = df_instance.shape
drivers = []
# n_cars = df_instance.shape[0] - deficit
for i in range(0, n_cars):
    column_name = 'car_' + str(i)
    drivers.append(column_name)
    dis_to_pickup = np.random.lognormal(estimated_mu, estimated_sigma, l)
    df_instance[column_name] = dis_to_pickup


df_instance['price'] = 0.0
def price(trip):
    price = (0.30 * trip["trip_distance"] + 0.25 * (trip["trip_duration_second"]/60)) + 5
    return price

df_instance['price'] = df_instance.apply(lambda row: price(row), axis=1 )

def cost(trip, driver):
    revenue = (trip["trip_distance"] + trip[driver])*0.1 - trip["price"]
    return revenue


for driver in drivers:
    df_instance[driver] = df_instance.apply(lambda row: cost(row, driver), axis=1 )

df_instance.drop(["price", "trip_distance", "trip_duration_second"], axis=1, inplace=True)
df_instance.reset_index(inplace=True, drop=True)

t_matrix = df_instance.values.T

cost_matrix = df_instance.values.T

row_ind, col_ind = linear_sum_assignment(cost_matrix)
assign_revenue = abs(cost_matrix[row_ind, col_ind]).sum()
print(assign_revenue)

def tree_propagation(assignment, available_passengers, available_cars, total_cost):
    if len(available_cars) == 0:
        return total_cost

    passenger_choice = available_passengers[round(int(len((available_passengers)) - 1) * assignment[0])]
    current_cost = cost_matrix[available_cars[0]][passenger_choice]

    assignment.pop(0); available_passengers.remove(passenger_choice); available_cars.pop(0)
    total_cost = tree_propagation(assignment, available_passengers, available_cars, total_cost)

    return total_cost + current_cost

def cost_function2(coords):
    answer_list = []
    passengers = [i for i in range(cost_matrix.shape[1])]
    cars = [i for i in range(cost_matrix.shape[0])]
    for coord in coords:
        coord = coord.tolist()
        answer_list.append(tree_propagation(coord.copy(), passengers.copy(), cars.copy(), total_cost = 0))
    return answer_list

from pyswarms.backend.topology import Random 
from random import random
my_topology = Random(static=False)

lower_bound = [0 for _ in range(cost_matrix.shape[0])]
upper_bound = [1 for _ in range(cost_matrix.shape[0])]

my_bounds = (np.array([lower_bound]), np.array([upper_bound]))

options = {'c1': 0.5, 'c2': 0.3, 'w':0.5}
optimizer = ps.single.GlobalBestPSO(n_particles=50, dimensions=cost_matrix.shape[0], options=options, bounds=my_bounds)

cost, pos = optimizer.optimize(cost_function2, iters=100)

from pyswarms.utils.functions.single_obj import sphere
from pyswarms.utils.plotters import plot_cost_history

cost_history = optimizer.cost_history

plot_cost_history(cost_history)
plt.show()