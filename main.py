import random
import matplotlib.pyplot as plt


def sq_distance(a, b):
    x_dif = a[0]-b[0]
    y_dif = a[1]-b[1]
    return x_dif*x_dif+y_dif*y_dif


def generate_random_points(D, n1, n2 , alpha):

    points = []
    actual_points = []
    sq_size = 1/D
    for i in range(D):
        for j in range(D):
            x_min = sq_size*i
            x_max = sq_size+x_min
            y_min = sq_size*j
            y_max = sq_size+y_min

            points_in_current_group = n1
            curgroup = random.choice([1, 2])
            if curgroup == 2:
                points_in_current_group = n2

            for _ in range(points_in_current_group):
                x_cord = random.uniform(x_min, x_max)
                y_cord = random.uniform(y_min, y_max)
                points.append([x_cord, y_cord])
                actual_points.append([x_cord, y_cord])
            if curgroup == 1:
                for _ in range(int((n1*(alpha))/(100-alpha))):
                    x_cord = random.uniform(x_min, x_max)
                    y_cord = random.uniform(y_min, y_max)
                    actual_points.append([x_cord, y_cord])
    return points , actual_points


def generate_k_clusters(k, points):
    centroids = [[random.uniform(0, 1), random.uniform(0, 1)]
                 for _ in range(k)]
    change = True
    n = len(points)
    cluster = [0 for i in range(n)]

    sqdis = n
    sq_dis_for_each_cluster = []

    for i in range(k):
        sq_dis_for_each_cluster.append(0)
    while change:
        current = 0
        change = False
        new_centroids = []
        count_points = []
        for i in range(k):
            sq_dis_for_each_cluster[i] = 0
            new_centroids.append([0, 0])
            count_points.append(0)
        for j in range(n):
            point = points[j]
            min_distance_cluster = 0
            min_distance = 1
            for i in range(k):
                centroid = centroids[i]
                if sq_distance(point, centroid) < min_distance:
                    min_distance = sq_distance(point, centroid)
                    min_distance_cluster = i

            cluster[j] = min_distance_cluster
            current += min_distance

            sq_dis_for_each_cluster[min_distance_cluster] += min_distance
            new_centroids[min_distance_cluster][0] += point[0]
            new_centroids[min_distance_cluster][1] += point[1]
            count_points[min_distance_cluster] += 1

        for i in range(k):
            if (count_points[i] != 0):
                new_centroids[i][0] /= count_points[i]
                new_centroids[i][1] /= count_points[i]

        if current < sqdis:
            change = True
            sqdis = current
            centroids = new_centroids
    # sum =0
    # for i in sq_dis_for_each_cluster:
    #     sum +=i
    return cluster, centroids


if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))
  #  k = int(input("Enter the number of clusters: ")) 
   # k is now taken as a function of the number of points in the dataset
    # alpha = float(input("Enter the percentage of first density that is under-reported: "))
    cost = []
    for alpha in range(10,100,10):
        k1 = max(1 ,int((D*D*(n1+n2))/50))
        k2 = max(1, int((D*D*(n1  + int((alpha*n1)/(100-alpha)) + n2))/50))
        points , actual_points = generate_random_points(D, n1, n2 , alpha)
    # actual_points = generate_random_points(D, n1  + int((alpha*n1)/100), n2)
        cluster, centroids  = generate_k_clusters(k1, points)
        actual_cluster, actual_centroids = generate_k_clusters(k2, actual_points)
        sum_of_squares = 0
        actual_sum_of_squares = 0
        for point in actual_points:
            mini =1
            for cen in centroids:
                mini = min(mini, sq_distance(cen, point))
            sum_of_squares += mini
        # for point in actual_points:
        #     mini =1
        #     for cen in actual_centroids:
        #         mini = min(mini, sq_distance(cen, point))
        #     actual_sum_of_squares += mini

        # estimated_cluster = actual_cluster[:]
        # for i in range(len(actual_cluster)):
        #     point = actual_points[i]
        #     mini = 1
        #     cent = -1
        #     for j in range(len(centroids)):
        #         dista = sq_distance(centroids[j], point)
        #         if dista < mini:
        #             mini = dista
        #             cent = j
        #     estimated_cluster[i] = cent
        # cluster_colors = []
        # actual_cluster_colors = []
        # for _ in range(k1):
        #     cluster_colors.append('#%06X' % random.randint(0, 0xFFFFFF))
        # for _ in range(k2):
        #     actual_cluster_colors.append('#%06X' % random.randint(0, 0xFFFFFF))
        # print(centroids)
        # print(actual_centroids)
        # print(sum_of_squares)
        # print(actual_sum_of_squares)
        cost.append(sum_of_squares)
        
        #figure, axis = plt.subplots(1,2)

        # axis[0].scatter([point[0] for point in actual_points], [point[1] for point in actual_points], color=[
        #             cluster_colors[estimated_cluster[i]] for i in range(len(actual_points))])
        # axis[0].scatter([centroid[0] for centroid in centroids], [centroid[1]
        #                                                     for centroid in centroids], color=['blue'])
        # axis[0].set_title("under-reported graph")
        # axis[1].scatter([point[0] for point in actual_points], [point[1] for point in actual_points], color=[
        #             actual_cluster_colors[actual_cluster[i]] for i in range(len(actual_points))])
        # axis[1].scatter([centroid[0] for centroid in actual_centroids], [centroid[1]
        #                                                     for centroid in actual_centroids], color=['blue'])    
        # axis[1].set_title("Actual graph")
        # plt.show()
    plt.plot(range(10,100,10), cost)
    plt.show()