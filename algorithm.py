import pandas as pd
from itertools import combinations
from geopy.distance import geodesic


def neighbour(cities, start, visited, distances):
    df1 = distances.loc[(distances.city1 == start) & (
        distances.city2.isin([item for item in cities.city if item not in visited]))].copy()
    df2 = distances.loc[(distances.city2 == start) & (
        distances.city1.isin([item for item in cities.city if item not in visited]))].copy()
    res = pd.Series(data=list(df1.dist) + list(df2.dist), index=list(df1.city2) + list(df2.city1))
    print(res)
    return (res.idxmin())


def get_distancies(cities):
    cities1, cities2, distances = [], [], []
    for city1, city2 in combinations(list(cities.city), 2):
        cities1.append(city1)
        cities2.append(city2)
        g_city1 = (cities.at[city1, 'lat'], cities.at[city1, 'long'])
        g_city2 = (cities.at[city2, 'lat'], cities.at[city2, 'long'])
        distances.append(geodesic(g_city1, g_city2).km)

    return pd.DataFrame({'city1': cities1, 'city2': cities2, 'dist': distances})


def find_path(cities, start, finish):
    sequence = []
    df_dist = get_distancies(cities)
    current = start
    while len([start] + sequence + [finish]) < len(cities):
        current = neighbour(cities, current, [start] + sequence + [finish], df_dist)
        sequence.append(current)

    return [start] + sequence + [finish]