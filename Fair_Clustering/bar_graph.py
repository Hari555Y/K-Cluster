from fair_cluster import generate_fair_k_clusters, sq_distance, generate_random_points, cost
import matplotlib.pyplot as plt
import random

if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))

    reported_points, actual_points, groups = generate_random_points(D, n1, n2, 0)

    priviledged_cost = []
    unpriviledged_cost = []
    total_cost = []

    alphas = [(10*i, 100-10*i) for i in range(1,6)]
    for alpha in alphas:
    
        points = []
        cur_point = 0

        for i in range(D):
            for j in range(D):
                cur_group = groups[i][j]
                if cur_group == 2:
                    num_points_group = n2

                    for l in range(num_points_group):
                        point = actual_points[cur_point]
                        cur_point += 1
                        points.append(point)

                else:
                    p = random.choice([0,1])
                    num_points_group = int(n1*(100-alpha[p])/100)
                    for l in range(num_points_group):
                        point = actual_points[l+cur_point]
                        points.append(point)
                    cur_point += n1


        k_reported = max(1, int(len(points)/1000))
        partition, centroids = generate_fair_k_clusters(k_reported, points)
        
        upc, pc, tc = cost(partition, centroids, k_reported)
        unpriviledged_cost.append(upc)
        priviledged_cost.append(pc)
        total_cost.append(tc)
    
    x1 = [-0.2, 0.8, 1.8, 2.8, 3.8]
    x2 = [0.2, 1.2, 2.2, 3.2, 4.2]
    ax = plt.subplot()
    ax.bar(x1, unpriviledged_cost, 0.4, label='Unpriviledged Cost')
    ax.bar(x2, priviledged_cost, 0.4, label='Priviledged Cost')
    ax.set_xticks(range(5))
    ax.set_xticklabels(alphas)
    plt.legend()
    plt.show()