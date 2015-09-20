import numpy as np
np.zeros([30000, 2000])
len(np.zeros([30000, 2000]))
filename = 'feature_db-files.txt'
file = open(filename)

empty_list =[]   

for line in file:
    splitted_line = line.split(') {')

    useful_part = splitted_line[1]
    useful_part = useful_part[:-2]
    new_split = useful_part.split(', ')

    num_list =[]   
    for b in new_split:
       c = b.split(': ')[1]
       num_list.append(float(c))
    empty_list.append(num_list) 

A = np.array(empty_list)

from sklearn.cluster import KMeans

for no_of_clusters in range(2,20):
    kmeans = KMeans(n_clusters=no_of_clusters)
    kmeans.fit(A)

    j = [0]*no_of_clusters

    for i in kmeans.predict(A): 
        j[i] = j[i]+1

    print j






    
    
    
    
    

