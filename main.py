import random
import matplotlib.pyplot as plt

def sq_distance(a, b):
    x_dif = a[0]-b[0]
    y_dif = a[1]-b[1]
    return x_dif*x_dif+y_dif*y_dif

def generate_random_points(D, n1, n2):

    points = []
    sq_size = 1/D
    for i in range(D):
        for j in range(D):
            x_min = sq_size*i
            x_max = sq_size+x_min
            y_min = sq_size*j
            y_max = sq_size+y_min
            
            points_in_current_group = n1
            curgroup = random.choice([1,2])
            if curgroup==2:
                points_in_current_group = n2
            
            for _ in range(points_in_current_group):
                x_cord = random.uniform(x_min, x_max)
                y_cord = random.uniform(y_min, y_max)
                points.append([x_cord,y_cord])
    
    return points

def generate_k_clusters(k, points):
    centroids = [[random.uniform(0,1), random.uniform(0,1)] for _ in range(k)]
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
            new_centroids.append([0,0])
            count_points.append(0)
        for j in range(n):
            point = points[j]
            min_distance_cluster = 0
            min_distance = 1
            for i in range(k):
                centroid = centroids[i]
                if sq_distance(point, centroid)<min_distance:
                    min_distance = sq_distance(point, centroid)
                    min_distance_cluster = i

            cluster[j] = min_distance_cluster
            current += min_distance

            sq_dis_for_each_cluster[min_distance_cluster] += min_distance
            new_centroids[min_distance_cluster][0] += point[0]
            new_centroids[min_distance_cluster][1] += point[1]
            count_points[min_distance_cluster] += 1
        
        for i in range(k):
            if(count_points[i]!=0):
                new_centroids[i][0] /= count_points[i]
                new_centroids[i][1] /= count_points[i]
        
        if current<sqdis:
            change = True
            sqdis = current
            centroids = new_centroids
    
    return cluster, centroids
    

if __name__=='__main__':
    points = generate_random_points(2,5,3)
    cluster, centroids = generate_k_clusters(3,points)
    colors = ['blue','red','green']
    centcolor = ['yellow','black','orange']
    print(centroids)
    plt.scatter([point[0] for point in points], [point[1] for point in points], color=[colors[cluster[i]] for i in range(len(points))])
    plt.scatter([centroid[0] for centroid in centroids], [centroid[1] for centroid in centroids], color=[centcolor[i] for i in range(len(centcolor))])
    plt.show()