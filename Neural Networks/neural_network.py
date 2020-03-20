#Juan Diego Gonzalez German
#1001401837
#10/10/19

import numpy as np
import math
import sys

#get arguments
training_file = sys.argv[1]
test_file = sys.argv[2]
layers = int(sys.argv[3])
upl = int(sys.argv[4])
R = int(sys.argv[5])

#load data from files
training_data = np.loadtxt(training_file)
test_data = np.loadtxt(test_file)

#functions go here:
def split_data(data): #and normalize it
    attributes  = [row[:-1] for row in data]
    classes = [int(row[-1]) for row in data]
    maxv = np.amax(attributes)
    attributes = attributes/maxv
    return attributes, classes

def sigmoid(x):
    x = np.clip(x, -500, 500)
    return 1/(1 + math.exp(-x))

def get_layer_index(l, prev_start, layers, upl):
    prev_count = upl
    if l == 1:
        prev_count = number_of_attributes
        
    curr_count = upl
    if l == layers - 1:
        curr_count = number_of_classes   
    
    curr_start = prev_start + prev_count
    curr_end = curr_start + curr_count
    
    return curr_start, curr_end

def initiate_weights(layers,upl):
    w = {}
    prev_start = 1
    for l in range(1,layers):
        curr_start, curr_end = get_layer_index(l, prev_start, layers, upl)
        for j in range(curr_start, curr_end):
            w[(0,j)] = np.random.uniform(-0.05,0.05)
            for i in range(prev_start, curr_start):
                w[(i,j)] = np.random.uniform(-0.05,0.05)
        prev_start = curr_start
    return w

def find_connections(w, j, back):
    pos = 1
    connections = []
    if back == True:
        pos = 0
    for key in w.keys():
        if key[pos] == j:
            connections.append(key[pos-1])
    connections.sort()
    return connections

def run_nn(z,w,U):
    a = np.zeros(U)
    for j in range(number_of_attributes+1,U):
        j_connections = find_connections(w,j,False)
        for i in j_connections:
            a[j] += w[(i,j)]*z[i]
        z[j] = sigmoid(a[j])
    return z

def find_sigma(z,w,U,t,r):
    o = np.zeros(U)
    for j in range(r, U):
            o[j] = (z[j] - t[j-r])*(z[j])*(1 - z[j])
    for j in range(r-1, number_of_attributes, -1):
        t1 = 0
        j_connections_forward = find_connections(w,j,True)
        for u in j_connections_forward:
            t1 += w[(j,u)]*o[u]
        o[j] = (t1)*(z[j])*(1 - z[j])
    return o

def update_weights(z,w,U,o,n):
    for j in range(number_of_attributes+1,U):
        j_connections = find_connections(w,j,False)
        for i in j_connections:
            w[(i,j)] -= n*o[j]*z[i]
    return w

#find number of inputs per object, and no of objects
data_size = training_data.shape
number_of_objects = data_size[0]
number_of_attributes = data_size[1]-1

#split data, find number of classes
training_data, classes = split_data(training_data)
class_list = list(set(classes))
number_of_classes = len(class_list)
test_data, tclasses = split_data(test_data)

#calculate weights and find edges
w = initiate_weights(layers, upl)
hidden_l = layers - 2
U = number_of_attributes + (hidden_l*upl) + number_of_classes + 1
r = U - number_of_classes
n = 1

for training_round in range(R):
    index = -1
    for entry in training_data:
        t = np.zeros(number_of_classes)
        index += 1
        k = classes[index]
        for i in range(len(class_list)):
            if k == class_list[i]:
                t[i] = 1

        z = np.zeros(U)
        z[0] = 1
        z[1:number_of_attributes+1] = entry
        
        #update outputs
        z = run_nn(z,w,U)
        
        #get sigmas
        o = find_sigma(z,w,U,t,r)

        #update_weights
        w = update_weights(z,w,U,o,n)

    n *= 0.98

tdata_size = test_data.shape
number_of_objects = tdata_size[0]

#Classification
total_acc = 0
index = -1
for entry in test_data:   
    index += 1    
    
    z = np.zeros(U)
    z[0] = 1
    z[1:number_of_attributes+1] = entry[:]
    z = run_nn(z,w,U)
    tn = z[r:]   
    
    maxval = np.amax(tn)
    real_class = tclasses[index]
    hits = []
    
    for p in range(len(tn)):
         if tn[p] == maxval:
             hits.append(class_list[p])
    
    acc = 0
    prediction = hits[0]            
    if len(hits) <= 1 and prediction == real_class:
        acc = 1
    elif real_class in hits:
        acc = 1/len(hits)
    
    print('ID={:5d}, predicted={:3d}, true={:3d}, accuracy={:4.2f}'.format(index,prediction,real_class,acc))
           
    total_acc += acc
    
print('classification accuracy={:6.4f}'.format(total_acc/number_of_objects))  