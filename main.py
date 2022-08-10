import random
from unicodedata import name
from matplotlib.colors import PowerNorm
import matplotlib.pyplot as plt
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

def generate_k_clusters(k, D, n1, n2):
    points = generate_random_points(D, n1, n2)
    

if __name__=='__main__':
    points = generate_random_points(5,1,20)
    plt.scatter([point[0] for point in points], [point[1] for point in points])
    plt.show()