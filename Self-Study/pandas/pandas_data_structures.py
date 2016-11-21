import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('max_columns', 50)
# %matplotlib inline

# Series

# create a Series with an arbitrary list
s = pd.Series([7, 'Heisenberg', 3.14, -1789710578, 'Happy Eating!'])
print(s)
s = pd.Series([7, 'Heisenberg', 3.14, -1789710578, 'Happy Eating!'], index=['A', 'Z', 'C', 'Y', 'E'])
print(s)

# The Series constructor can convert a dictonary as well, using the keys of the dictionary as its index.
d = {'Chicago': 1000, 'New York': 1300, 'Portland': 900, 'San Francisco': 1100, 'Austin': 450, 'Boston': None}
cities = pd.Series(d)
print(cities)

# You can use the index to select specific items from the Series
print(cities['Chicago'])
print(cities[['Chicago', 'Portland', 'San Francisco']])
# Or you can use boolean indexing for selection.
print(cities[cities < 1000])
# That last one might be a little weird, so let's make it more clear - cities < 1000
# returns a Series of True/False values, which we then pass to our Series cities,
# returning the corresponding True items.
less_than_1000 = cities < 1000
print(less_than_1000)
print('\n')
print(cities[less_than_1000])

# changing based on the index
print('Old value:', cities['Chicago'])
cities['Chicago'] = 1400
print('New value:', cities['Chicago'])
# changing values using boolean logic
print(cities[cities < 1000])
print('\n')
cities[cities < 1000] = 750
print(cities[cities < 1000])

print('Seattle' in cities)
print('San Francisco' in cities)

# Mathematical operations can be done using scalars and functions.
# divide city values by 3
print(cities / 3)
# square city values
print(np.square(cities))

# You can add two Series together,
# which returns a union of the two Series with the addition occurring on the shared index values.
# Values on either Series that did not have a shared index will produce a NULL/NaN (not a number).
print(cities[['Chicago', 'New York', 'Portland']])
print('\n')
print(cities[['Austin', 'New York']])
print('\n')
print(cities[['Chicago', 'New York', 'Portland']] + cities[['Austin', 'New York']])

# returns a boolean series indicating which values aren't NULL
print(cities.notnull())
# use boolean logic to grab the NULL cities
print(cities.isnull())
print('\n')
print(cities[cities.isnull()])

# DataFrame

