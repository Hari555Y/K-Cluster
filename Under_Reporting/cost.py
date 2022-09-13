import matplotlib.pyplot as plt
from bias import generate_k_clusters, generate_random_points
from main import sq_distance


if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))

    reported_points, actual_points, groups = generate_random_points(D, n1, n2, 0)

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
    plt.plot(range(90, 0, -10), cost)
    plt.show()
