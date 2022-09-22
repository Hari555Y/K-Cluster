from cProfile import label
import matplotlib.pyplot as plt
from bias import generate_k_clusters, generate_random_points, sq_distance


if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))

    reported_points, actual_points, groups = generate_random_points(D, n1, n2, 0)

    priviledged_cost = []
    unpriviledged_cost = []
    total_cost = []
    # k_values = []
    alpha = 50
    for k_reported in range(90, 0, -10):
    
        reported_points = []
        # k_reported = max(1, int(len(reported_points)/1000))
        k_actual = max(1 ,int(k_reported*2))
        # k_values.append(k_actual)
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

        sum_of_squares_priviledged = 0
        sum_of_squares_unpriviledged = 0

        cur_point = 0

        for i in range(D):
            for j in range(D):
                cur_group = groups[i][j]
                num_points_group = n1
                if cur_group == 2:
                    num_points_group = n2

                for l in range(num_points_group):
                    point = actual_points[cur_point]
                    cur_point += 1
                    mini = 1
                    for j in range(len(reported_centroids)):
                        dista = sq_distance(reported_centroids[j], point)
                        if dista < mini:
                            mini = dista
                    
                    if cur_group == 2:
                        sum_of_squares_priviledged += mini
                    else:
                        sum_of_squares_unpriviledged += mini

        priviledged_cost.append(sum_of_squares_priviledged)
        unpriviledged_cost.append(sum_of_squares_unpriviledged)
        total_cost.append(sum_of_squares_priviledged+sum_of_squares_unpriviledged)

    
    # plt.figure(1, figsize= (10, 7))
    # plt.subplot(3,1,1)
    plt.title("Priviledged Group Cost")
    plt.xlabel("Value of k")
    plt.ylabel("Priviledged Cost")
    plt.plot(range(90 , 0, -10), priviledged_cost)

    # plt.subplot(3,1,2)
    # plt.title("UnPriviledged Group Cost")
    # plt.xlabel("percentage of density under-reported")
    # plt.ylabel("UnPriviledged Cost")
    # plt.plot(range(90, 0, -10), unpriviledged_cost)

    # plt.subplot(3,1,3)
    # plt.title("Total Cost")
    # plt.xlabel("percentage of density under-reported")
    # plt.ylabel("Total Cost")
    # plt.plot(range(90, 0, -10), total_cost)
    # plt.tight_layout()
    plt.show()
