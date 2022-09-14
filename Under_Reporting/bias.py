# K Clustering Algorithm when a Group shows Underreporting
import sys
import random
import matplotlib.pyplot as plt

sys.path.insert(0,'C:/Users/HARIKESH/Desktop/github/K-Cluster')
from main import sq_distance, generate_k_clusters


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

            curgroup = random.choice([1, 2])

            if curgroup==2:
                groups[i][j] = 2
                for _ in range(n2):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    points.append([x_cord, y_cord])
                    actual_points.append([x_cord, y_cord])

            else:
                num_points_reported = int((100-alpha) * n1 / 100)
                for _ in range(num_points_reported):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    points.append([x_cord, y_cord])
                    actual_points.append([x_cord, y_cord])
                
                for _ in range(n1 - num_points_reported):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    actual_points.append([x_cord, y_cord])

    return points , actual_points, groups



if __name__ == '__main__':
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))

    alpha = float(input("Enter the percentage of first density that is under-reported: "))
    
    reported_points , actual_points, groups = generate_random_points(D, n1, n2 , alpha)
    k_reported = max(1, int(len(reported_points)/1000))
    k_actual = max(1 ,int(len(actual_points)/1000))

    reported_cluster, reported_centroids  = generate_k_clusters(k_reported, reported_points)
    actual_cluster, actual_centroids = generate_k_clusters(k_actual, actual_points)

    reported_sum_of_squares = 0
    actual_sum_of_squares = 0

    estimated_cluster = actual_cluster[:]
    for i in range(len(actual_cluster)):
        point = actual_points[i]
        mini = 1
        cent = -1
        for j in range(len(reported_centroids)):
            dista = sq_distance(reported_centroids[j], point)
            if dista < mini:
                mini = dista
                cent = j
        estimated_cluster[i] = cent
        reported_sum_of_squares += mini

    for point in actual_points:
        mini =1
        for cen in actual_centroids:
            mini = min(mini, sq_distance(cen, point))
        actual_sum_of_squares += mini

    cluster_colors = []
    actual_cluster_colors = []
    for _ in range(k_reported):
        cluster_colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    for _ in range(k_actual):
        actual_cluster_colors.append('#%06X' % random.randint(0, 0xFFFFFF))

    print("Cost for underreported:", reported_sum_of_squares)
    print("Actual Cost:", actual_sum_of_squares)

    figure, axis = plt.subplots(1,2)

    axis[0].scatter([point[0] for point in actual_points], [point[1] for point in actual_points], color=[
                cluster_colors[estimated_cluster[i]] for i in range(len(actual_points))])
    axis[0].scatter([centroid[0] for centroid in reported_centroids], [centroid[1]
                                                          for centroid in reported_centroids], color=['blue'])
    axis[0].set_title("under-reported graph")
    axis[1].scatter([point[0] for point in actual_points], [point[1] for point in actual_points], color=[
                actual_cluster_colors[actual_cluster[i]] for i in range(len(actual_points))])
    axis[1].scatter([centroid[0] for centroid in actual_centroids], [centroid[1]
                                                          for centroid in actual_centroids], color=['blue'])    
    axis[1].set_title("Actual graph")
    plt.show()