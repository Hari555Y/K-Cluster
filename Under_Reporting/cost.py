import sys
import matplotlib.pyplot as plt
from bias import generate_k_clusters, generate_random_points
sys.path.insert(0,'D:\Semester7\COD492\K-Clustering')
from main import sq_distance


if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))

    cost = []
    for alpha in range(10, 100, 10):
    
        reported_points , actual_points = generate_random_points(D, n1, n2 , alpha)
        k_reported = max(1, int(len(reported_points)/1000))
        k_actual = max(1 ,int(len(actual_points)/1000))

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
        
    plt.title(f"Graph for {len(actual_points)} points")
    plt.xlabel("percentage of density under-reported")
    plt.ylabel("Cost of the algorithm")
    plt.plot(range(10, 100, 10), cost)
    plt.show()
