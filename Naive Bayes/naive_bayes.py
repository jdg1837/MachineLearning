#Juan Diego Gonzalez German
#1001401837
#09/12/19

import numpy as np
import sys

training_file = sys.argv[1]
test_file = sys.argv[2]

training_data = np.loadtxt(training_file)
test_data = np.loadtxt(test_file)

data_size = training_data.shape
number_of_objects = data_size[0]
number_of_attributes = data_size[1]-1

def find_gaussian(x,u,o):
    num = np.exp(-np.power(x-u,2)/(2*np.power(o,2)))
    den = o*np.sqrt(2*np.pi)
    return num/den

attribute_data = {}
class_count = [0] * int(np.amax(training_data[:,data_size[1]-1]))

for entry in training_data:
    entry_class = int(entry[-1])
    class_count[entry_class-1] += 1
    
    if entry_class not in attribute_data:
        attribute_data[entry_class] = []
        for i in range(number_of_attributes):
            attribute_data[entry_class].append([])
    for j in range(0,number_of_attributes):
        attribute_data[entry_class][j].append(entry[j])
  
#probability of class C      
pC = [x /  number_of_objects for x in class_count]

#i: class, j: attribute, z1: mean, z2: std 
class_values = {}
for keyclass in sorted(attribute_data):
    class_values[keyclass] = np.zeros((number_of_attributes,2))
#class_values = np.zeros((len(attribute_data),number_of_attributes,2))
for i in class_values:
    for j in range(0,number_of_attributes):
        x = attribute_data[i][j]
        mean = np.mean(x)
        class_values[i][j][0] = mean
        
        std = np.std(x)
        if std < 0.01:
            std = 0.01
        class_values[i][j][1] = std
        
        print('Class {:d}, attribute {:d}, mean = {:.2f}, std = {:.2f}'.format(i,j+1,mean,std))

data_size = test_data.shape
number_of_objects = data_size[0]
#Classification
total_acc = 0
id = 0
for entry in test_data:   
    id += 1    
    pCx = {}
    pxC_times_pC = {}
    px = 0
    count = 0
    for k in class_values:
        pxC = 1
        for i in range(number_of_attributes):
            xi = entry[i]
            u = class_values[k][i][0]
            o = class_values[k][i][1]
            pxC *= find_gaussian(xi,u,o)   
        px += pxC*pC[k-1]
        pxC_times_pC[k] = pxC*pC[k-1]
        
    for k in class_values:
        pCx[k] = pxC_times_pC[k]/px
        
    maxval = max(pCx.values())
    prediction = 0
    real_class = int(entry[-1])
    hits = []
    acc = 0
    
    for c in pCx:
        if pCx[c] == maxval:
            hits.append(c)
            prediction = c
    
    if len(hits) <= 1 and prediction == real_class:
            acc = 1
    elif real_class in hits:
           acc = 1/len(hits)
           print(3)
    print('ID={:5d}, predicted={:3d}, probability = {:.4f}, true={:3d}, accuracy={:4.2f}'.format(id,prediction,pCx[prediction],real_class,acc))
           
    total_acc += acc
    
print('classification accuracy={:6.4f}'.format(total_acc/number_of_objects))  