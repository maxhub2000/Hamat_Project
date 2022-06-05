from cv2 import polarToCart
import pandas as pd
import numpy as np


# d = {'col1': [1, 2], 'col2': [3, 4]}
# df1 = pd.DataFrame(data=d)


# e = {'col3': [7, 8], 'col4': [9, 10]}
# df2 = pd.DataFrame(data=e)


# print(df1,"\n",df2, "\n")

# tup = (df1, df2)

# print(tup[1]["col3"])



# a = 'a'
# b = 'b'
# c = 'c'

# LL = [a,b,c]

# df3 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
#                    columns=[a, b, c])


# list_of_dfs = []

# list_of_dfs.append(df1)
# list_of_dfs.append(df2)
# list_of_dfs.append(df3)

# print(type(list_of_dfs))


# print(type(list_of_dfs[0]))





# def adjacent(route, rnd):
#     n = len(route)
#     result = np.copy(route)
#     i = rnd.randint(n); j = rnd.randint(n)
#     tmp = result[i]
#     result[i] = result[j]; result[j] = tmp
#     return result


# rnd = np.random.RandomState(4)
# print(rnd)
# m_route = [1,2,3,4,5,6,7,8,9]

# print(adjacent(m_route, rnd ))




# fruits = ['apple', 'banana', 'orange', 'grape', "a", "b", "c", "d","e","f","g","h","k"]
# subset_size = int(0.7 * len(fruits))
# print(np.random.choice(fruits, 7, replace=False))




# def get_neighbors(route):
#     # choose 3 random unique indeces
#     indeces = np.random.choice(list(range(len(route))), 3, replace=False)
#     i,j,k = indeces[0], indeces[1], indeces[2]
#     # initialize neighbors list
#     neighbors = []
#     # initialize copies of route
#     new_route1, new_route2, new_route3 = route.copy(), route.copy(), route.copy()
#     # create new neighbors
#     new_route1[i],new_route1[j] =  route[j], route[i]
#     new_route2[j],new_route2[k] =  route[k], route[j]
#     new_route3[k],new_route3[i] =  route[i], route[k]
#     neighbors.extend([new_route1, new_route2, new_route3])
#     return neighbors


# print(get_neighbors(m_route))





mlm = [k*2+1 for k in range(190)]


for j in range(0, len(mlm), 20):
    start = j
    end = j + 20
    print(mlm[start:end])


    #print(len(mlm[start:end]))



lstt = ["max"]*4


[print(lstt)]




df = pd.DataFrame({'mass': [0.330, 4.87 , 5.97],
                   'radius': [2439.7, 6051.8, 6378.1]},
                  index=['Mercury', 'Venus', 'Earth'])
plot = df.plot.pie(y='mass', figsize=(5, 5))
print(plot)