from cProfile import label
from mip import *
import random
import matplotlib.pyplot as plt


def sq_distance(a, b):
    x_dif = a[0]-b[0]
    y_dif = a[1]-b[1]
    return x_dif*x_dif + y_dif*y_dif

def average_cost(points, centroids, frac):
    priviledged_cost = 0
    unpriviledged_cost = 0
    cost = 0

    priviledged_total = 0
    unpriviledged_total = 0
    r = len(points)
    n = len(centroids)

    for i in range(r):
        for j in range(n):
            val = frac[i][j]*sq_distance(points[i], centroids[j])
            cost += val
            if points[i][2] == 1:
                unpriviledged_total += 1
                unpriviledged_cost += val
            else:
                priviledged_total += 1
                priviledged_total += val
    
    return priviledged_cost/priviledged_total, unpriviledged_cost/unpriviledged_total, cost/r


def generate_random_points(D, n1, n2 , alpha):
    points = []
    actual_points = []
    groups = [[1 for i in range(D)] for j in range(D)] 
    sq_size = 1/D
    for i in range(D):
        for j in range(D):
            x_min = sq_size*i
            x_max = sq_size+x_min
            y_min = sq_size*j
            y_max = sq_size+y_min

            curgroup = 2
            if i==0 and j==0:
                curgroup = 1

            if curgroup==2:
                groups[i][j] = 2
                for _ in range(n2):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    points.append([x_cord, y_cord, 2])
                    actual_points.append([x_cord, y_cord, 2])

            else:
                num_points_reported = int((100-alpha) * n1 / 100)
                for _ in range(num_points_reported):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    points.append([x_cord, y_cord, 1])
                    actual_points.append([x_cord, y_cord, 1])
                
                for _ in range(n1 - num_points_reported):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    actual_points.append([x_cord, y_cord, 1])

    return points , actual_points, groups


def generate_k_clusters(k, reported_points):
    r = len(reported_points)

    T = 10

    g1 = sum(1 for i in range(r) if reported_points[i][2]==1)
    g2 = r-g1


    n = k
    centroids = [[random.uniform(0, 1), random.uniform(0, 1)] for _ in range(n)]
    frac = [[0 for i in range(n)] for j in range(r)]

    for t in range(T):
        
        m = Model("k_clustering")
        fractions = [[m.add_var(name = 'fraction', var_type = INTEGER, ub = 100, lb = 0) for i in range(n)]for j in range(r)]
        for j in range(r):
            m+= (xsum(fractions[j][i] for i in range(n))==100)

        for col in range(n):
            totalsum = xsum(fractions[row][col] for row in range (r))
            totalsum30percent = totalsum*(max(0, (g1/r) - 0.01))
            m+= xsum(fractions[row][col] for row in range(r) if reported_points[row][2] == 1) >= totalsum30percent



        for col in range(n):
            totalsum = xsum(fractions[row][col] for row in range (r))
            totalsum30percent = totalsum*(max(0, (g2/r) - 0.01))
            m+= xsum(fractions[row][col] for row in range(r) if reported_points[row][2] == 2) >= totalsum30percent

        m.objective = xsum((fractions[i][j]/100)*(sq_distance(centroids[j] , reported_points[i])) for i in range(r) for j in range(n))
        m.optimize()

        for j in range(n):
            for i in range(r):
                frac[i][j] = fractions[i][j]/100
        
        upc = 0.000001+sum(frac[i][j]*(sq_distance(centroids[j] , reported_points[i])) for i in range(r) for j in range(n) if reported_points[i][2]==1)
        tu = 0.000001+sum(1 for i in range(r) if reported_points[i][2]==1)
        pc = 0.000001+sum(frac[i][j]*(sq_distance(centroids[j] , reported_points[i])) for i in range(r) for j in range(n) if reported_points[i][2]==2)
        tp = 0.000002+r - tu
    
        
    return frac, centroids, upc/tu, pc/tp
        

D = int(input("Enter the number of cuts in unit length: "))
n1 = int(input("Enter the first density parameter: "))
n2 = int(input("Enter the second density parameter: "))

unp_costs = []
p_costs = []
costs = []
reported_points, actual_points, groups = generate_random_points(D, n1, n2, 0)
for alpha in range(90, 0, -10):
    reported_points = []
    cur_point = 0

    for i in range(D):
        for j in range(D):
            cur_group = groups[i][j]
            if cur_group == 2:
                num_points_group = n2

                for l in range(num_points_group):
                    point = actual_points[cur_point]
                    cur_point += 1
                    reported_points.append(point)

            else:
                num_points_group = int(n1*(100-alpha)/100)
                for l in range(num_points_group):
                    point = actual_points[l+cur_point]
                    reported_points.append(point)
                cur_point += n1
    
    k = max(1,len(reported_points)//100)
    frac, centroids, upc, pc = generate_k_clusters(k, reported_points)

    unp_costs.append(upc)
    p_costs.append(pc)


plt.plot(range(90,0,-10), p_costs, label='Priviledged Average Cost')
plt.plot(range(90,0,-10), unp_costs, label='Unpriviledged Average Cost')
plt.xlabel("Percentage Underreporting")
plt.ylabel("Average Cost")
plt.title("Average Cost vs Underreporting for both groups")
plt.legend()
plt.show()