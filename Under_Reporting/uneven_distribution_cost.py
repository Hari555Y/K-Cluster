import matplotlib.pyplot as plt
import random
from bias import generate_k_clusters, sq_distance

def generate_random_points(D, n, alpha, underpriviledge_percent):

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

            group = random.uniform(0,1)

            curgroup = 1
            if group >= underpriviledge_percent/100:
                curgroup = 2

            if curgroup==2:
                groups[i][j] = 2
                for _ in range(n):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    points.append([x_cord, y_cord])
                    actual_points.append([x_cord, y_cord])

            else:
                num_points_reported = int((100-alpha) * n / 100)
                for _ in range(num_points_reported):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    points.append([x_cord, y_cord])
                    actual_points.append([x_cord, y_cord])
                
                for _ in range(n - num_points_reported):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    actual_points.append([x_cord, y_cord])

    return points , actual_points, groups

if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n = int(input("Enter the Density parameter: "))
    underpriviledge_percent = float(input("Percentage of Underpriviledged Groups: "))

    reported_points, actual_points, groups = generate_random_points(D, n, 0, underpriviledge_percent)

    cost = []
    for alpha in range(90, 0, -10):
    
        reported_points = []
        k_reported = max(1, int(len(reported_points)/1000))
        k_actual = max(1 ,int(len(actual_points)/1000))

        cur_point = 0

        for i in range(D):
            for j in range(D):
                cur_group = groups[i][j]
                if cur_group == 2:

                    for l in range(n):
                        point = actual_points[cur_point]
                        cur_point += 1
                        reported_points.append(point)

                else:
                    num_points_group = int(n*(100-alpha)/100)
                    for l in range(num_points_group):
                        point = actual_points[l+cur_point]
                        reported_points.append(point)
                    cur_point += n

        reported_cluster, reported_centroids  = generate_k_clusters(k_reported, reported_points)
        actual_cluster, actual_centroids = generate_k_clusters(k_actual, actual_points)

        reported_sum_of_squares = 0

        for i in range(len(actual_cluster)):
            point = actual_points[i]
            mini = 1
            for j in range(len(reported_centroids)):
                dista = sq_distance(reported_centroids[j], point)
                if dista < mini:
                    mini = dista
            reported_sum_of_squares += mini

        cost.append(reported_sum_of_squares)
        
    plt.title(f"Graph for {len(actual_points)} points with {underpriviledge_percent}% groups Underpriviledged")
    plt.xlabel("percentage of density under-reported")
    plt.ylabel("Cost of the algorithm")
    plt.plot(range(90, 0, -10), cost)
    plt.show()
