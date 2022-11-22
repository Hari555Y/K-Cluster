from math import sqrt
import sys
import random

from matplotlib import pyplot as plt

sys.path.insert(0,'C:/Users/HARIKESH/Desktop/K-Clustering/Under_Reporting')
from bias import generate_random_points
from main import sq_distance

def generate_fair_k_clusters(k, points):
    centroids = [[random.uniform(0, 1), random.uniform(0, 1)]
                 for _ in range(k)]
    change = True
    n = len(points)

    sqdis = n
    sq_dis_for_each_cluster = []

    for i in range(k):
        sq_dis_for_each_cluster.append(0)
    
    while change:
        current = 0
        change = False
        partition = [[] for i in range(k)]

        for i in range(k):
            sq_dis_for_each_cluster[i] = 0
            
        for j in range(n):
            point = points[j]
            min_distance_cluster = 0
            min_distance = 1
            for i in range(k):
                centroid = centroids[i]
                if sq_distance(point, centroid) < min_distance:
                    min_distance = sq_distance(point, centroid)
                    min_distance_cluster = i

            partition[min_distance_cluster].append(point)
            current += min_distance

            sq_dis_for_each_cluster[min_distance_cluster] += min_distance

        if current < sqdis:
            change = True
            sqdis = current
            centroids = line_cluster(points, partition, k)
        
        partition = [[] for i in range(k)]
        for j in range(n):
            point = points[j]
            min_distance_cluster = 0
            min_distance = 1
            for i in range(k):
                centroid = centroids[i]
                if sq_distance(point, centroid) < min_distance:
                    min_distance = sq_distance(point, centroid)
                    min_distance_cluster = i

            partition[min_distance_cluster].append(point)
            current += min_distance

            sq_dis_for_each_cluster[min_distance_cluster] += min_distance

    return partition, centroids


def line_cluster(points, partition, k):
    points_a = []
    points_b = []

    A = []
    B = []
    avga = []
    avgb = []
    line_size = []
    
    for point in points:
        if point[2] == 1:
            points_a.append(point)
        else:
            points_b.append(point)

    for i in range(k):
        U = partition[i]
        type_a = []
        type_b = []
        mean_a = [0,0]
        mean_b = [0,0]

        for point in U:
            if point[2] == 1:
                type_a.append(point)
                mean_a[0] += point[0]
                mean_a[1] += point[1]

            else:
                type_b.append(point)
                mean_b[0] += point[0]
                mean_b[1] += point[1]

        if len(type_a) == 0:
            mean_a[0] = mean_b[0]/len(type_b)
            mean_a[1] = mean_b[1]/len(type_b)
        else:
            mean_a[0] /= len(type_a)
            mean_a[1] /= len(type_a)

        if len(type_b)==0:
            mean_b[0] = mean_a[0]
            mean_b[1] = mean_a[1]
        
        else:
            mean_b[0] /= len(type_b)
            mean_b[1] /= len(type_b)
        
        a = len(type_a)/len(points_a)
        b = len(type_b)/len(points_b)
        line_length = sqrt(sq_distance(mean_a, mean_b))

        A.append(a)
        B.append(b)
        avga.append(mean_a)
        avgb.append(mean_b)
        line_size.append(line_length)

    T = 100
    y = 0.5
    for t in range(T):
        x = []
        for i in range(k):
            xi = ((1-y)*B[i]*line_size[i])/(y*A[i] + ((1-y)*B[i]))
            x.append(xi)
        
        v1a, v1b = grad_function(k, A, B, line_size, x)
        v2a, v2b = sum_squared_distance(partition, k, avga, avgb)
        fa = v1a+v2a
        fb = v1b+v2b

        if fa > fb:
            y += 1/pow(2, t+2)
        elif fa < fb:
            y -= 1/pow(2, t+2)
        else:
            break

    centroids = []
    for i in range(k):
        centix = ((line_size[i]-x[i])*avga[i][0] + (x[i]*avgb[i][0]))/line_size[i]
        centiy = ((line_size[i]-x[i])*avga[i][1] + (x[i]*avgb[i][1]))/line_size[i]
        centroids.append([centix, centiy])
    
    return centroids


def grad_function(k, A, B, line_size, x):

    grada = 0
    gradb = 0

    for i in range(k):
        grada += A[i]*x[i]*x[i]
        gradb += B[i]*(line_size[i]-x[i])*(line_size[i]-x[i])
    
    return grada, gradb


def sum_squared_distance(partition, k, avga, avgb):
    tot_a = 0
    tot_b = 0
    suma = 0
    sumb = 0

    for i in range(k):
        U = partition[i]

        for point in U:
            if point[2] == 1:
                tot_a += 1
                suma += sq_distance(point, avga[i])

            else:
                tot_b += 1
                sumb += sq_distance(point, avgb[i])

    
    suma /= tot_a
    sumb /= tot_b

    return suma, sumb

def cost(partition, centroids, k):
    total_a = 0
    total_b = 0
    total = 0
    sum_a = 0
    sum_b = 0
    summ = 0
    for i in range(k):
        part = partition[i]
        for point in part:
            if point[2] == 1:
                total_a += 1
                sum_a += sq_distance(point, centroids[i])
            else:
                total_b += 1
                sum_b += sq_distance(point, centroids[i])
            
            summ += sq_distance(point, centroids[i])
            total += 1
    
    return sum_a/total_a, sum_b/total_b, summ/total


if __name__ == "__main__":
    D = int(input("Enter the number of cuts in unit length: "))
    n1 = int(input("Enter the first density parameter: "))
    n2 = int(input("Enter the second density parameter: "))

    reported_points, actual_points, groups = generate_random_points(D, n1, n2, 0)

    priviledged_cost = []
    unpriviledged_cost = []
    total_cost = []
    for alpha in range(90, 0, -10):
    
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
                    num_points_group = int(n1*(100-alpha)/100)
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
    

    plt.plot(range(90,0,-10), unpriviledged_cost, label='Unpriviledged Cost')
    plt.plot(range(90,0,-10), priviledged_cost, label='Priviledged Cost')
    plt.xlabel("Percentage Density Underreporting")
    plt.ylabel("Average Cost")
    plt.title("Average Cost vs Underreporting for Both the Groups")
    plt.legend()
    plt.show()