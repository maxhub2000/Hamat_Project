import matplotlib.pyplot as plt
import numpy as np
from tsp import two_opt, path_distance

# 2-opt algorithm implementation
# https://stackoverflow.com/questions/25585401/travelling-salesman-in-scipy

if __name__ == '__main__':
    # Create a matrix of cities, with each row being a location in 2-space (function works in n-dimensions).
    cities = np.random.RandomState(42).rand(70,2)
    ##### MAX LINES:
    print("cities:\n", cities[0], " ", cities[3])
    print(cities[0][0])
    print(list(cities))
    y_low, y_high = 4.0, 44

    hamat_cities = np.array([[16, 5],[14, 9],[10, 13], [8, 11], [14, 5], [14, 9], [4, 5], [18, 5], [10, 13], [8, 5]])
    cities = hamat_cities.copy()

    # Find a good route with 2-opt ("route" gives the order in which to travel to each city by row number.)
    route, route_distance = two_opt(cities, 0.001, y_low, y_high )


    print("Route: " + str(route) + "\n\nDistance: " + str(route_distance))


    # # Find a good route with 2-opt ("route" gives the order in which to travel to each city by row number.)
    # route = two_opt(cities, 0.001, y_low, y_high )

    # # Reorder the cities matrix by route order in a new matrix for plotting.
    # new_cities_order = np.concatenate((np.array([cities[route[i]] for i in range(len(route))]),np.array([cities[0]])))
    # # Plot the cities.
    # plt.scatter(cities[:,0],cities[:,1])
    # # Plot the path.
    # plt.plot(new_cities_order[:,0],new_cities_order[:,1])
    # plt.show()
    # Print the route and the total distance travelled by the path.
    # print("Route: " + str(route) + "\n\nDistance: " + str(path_distance(route,cities)))



