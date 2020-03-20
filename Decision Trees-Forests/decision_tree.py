#Juan Diego Gonzalez German
#1001401837
#10/31/19

import numpy as np
import random
import sys

#loading and preparation
training_file = sys.argv[1]
test_file = sys.argv[2]
option = sys.argv[3]
pruning_thr = int(sys.argv[4])

training_data = np.loadtxt(training_file)
test_data = np.loadtxt(test_file)

data_size = training_data.shape
number_of_attributes = data_size[1]-1
tdata_size = test_data.shape
number_of_objects = tdata_size[0]

tclass = [int(row[-1]) for row in training_data]
class_list = list(set(tclass))
max_class = np.amax(tclass)

#Define Tree
class Node:
    def __init__(self, id, feat, thr, gain):
        self.left = None
        self.right = None
        self.id = id
        self.feat = feat
        self.thr = thr
        self.gain = gain
        self.dist = []

def DTLTopLvl(examples, thr):
    attributes = list(range(number_of_attributes))
    default = distribution(examples)
    return DTL(examples, attributes, default, thr, 1)

def DTL(examples, attributes, default, pruning_thr, id):
    if (len(examples) < pruning_thr) or (len(examples) == 0):
        leaf = Node(id, -1, -1, 0)
        leaf.dist = default
        return leaf
    elif len(list(set([x[-1] for x in examples]))) == 1:
        prediction = int(examples[0][-1])
        dist = [0]*(max_class+1)
        dist[prediction] = 1
        leaf = Node(id, -1, -1, 0)
        leaf.dist = dist
        return leaf
    else:
        best_att, best_thr, max_gain = chooseAtt(examples,attributes)
        tree = Node(id, best_att, best_thr, max_gain)
        examples_l = list(filter(lambda x: x[best_att] < best_thr, examples))
        examples_r = list(filter(lambda x: x[best_att] >= best_thr, examples))
        dist = distribution(examples)
        tree.left = DTL(examples_l, attributes, dist, pruning_thr, 2*id)
        tree.right = DTL(examples_r, attributes, dist, pruning_thr, (2*id)+1)
        return tree

def distribution(examples):
    count = float(len(examples))
    class_count = [0]*(max_class+1)
    if count == 0:
        return class_count
    for x in examples: 
        class_count[int(x[-1])] += 1
    dist = [x / count for x in class_count]
    return dist

def chooseAtt(examples, attributes):
    max_gain = best_att = best_thr = -1
    optimized = (option == 'optimized')

    for att in attributes:
        if not optimized:
            att = random.choice(attributes)
        attribute_values = [x[att] for x in examples]
        L = min(attribute_values)
        M = max(attribute_values)
        for k in range(1,51):
            thr = L + (k*(M-L)/51)
            gain = infoGain(examples, att, thr)
            if gain > max_gain:
                max_gain = gain
                best_att = att
                best_thr = thr
        if not optimized:
            break

    return best_att, best_thr, max_gain

def infoGain(examples, att, thr):
    dist_n = distribution(examples)
    k_l = list(filter(lambda x: x[att] < thr, examples))
    dist_l = distribution(k_l)
    k_r = list(filter(lambda x: x[att] >= thr, examples))
    dist_r = distribution(k_r)
    return entropy(dist_n) - (len(k_l)/float(len(examples))*entropy(dist_l)) - (len(k_r)/float(len(examples))*entropy(dist_r))

def entropy(dist):
    H = 0
    for x in dist:
        if(x == 0):
            continue
        else:
            H -= x*np.log2(x)
    return H

def printTree(tree, tree_id):
    q = []
    q.append(tree)
    while(q):
        node = q.pop(0)
        print('tree={:2d}, node={:2d}, feature={:2d}, thr={:6.2f}, gain={:f}'.format(tree_id, node.id, node.feat, node.thr, node.gain))
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

def treeClassifier(test, node):
    feat = node.feat
    if feat == -1:
        return node.dist
    elif test[feat] < node.thr:
        return treeClassifier(test, node.left)
    else:
        return treeClassifier(test, node.right)

def forestAvg(forest_dist):
    forest_size = len(forest_dist)
    tdist = [0.0]*len(forest_dist[0])
    for tree in forest_dist:
        for class_id in range(len(tree)):
            tdist[class_id] += tree[class_id]
    return [x/forest_size for x in tdist]

#build forest and print it. A single tree is considered a forest of size 1
forest = []
rounds = 1
if option == 'forest3':
    rounds = 3
elif option == 'forest15':
    rounds = 15
for r in range(rounds):
    tree = DTLTopLvl(training_data, pruning_thr)
    forest.append(tree)
    printTree(tree, r+1)

#classify
total_acc = 0
i = -1
for test in test_data:   
    i += 1
    forest_dist = []
    for tree in forest:
        forest_dist.append(treeClassifier(test, tree))
    tdist = forestAvg(forest_dist)
    maxval = np.amax(tdist)
    real_class = int(test[-1])
    hits = []

    for p in range(len(tdist)):
        if tdist[p] == maxval:
            hits.append(p)

    acc = 0
    prediction = hits[0]            
    if len(hits) <= 1 and prediction == real_class:
        acc = 1
    elif real_class in hits:
        acc = 1/len(hits)
    total_acc += acc

    #print('ID={:5d}, predicted={:3d}, true={:3d}, accuracy={:4.2f}'.format(i,prediction,real_class,acc))
print('classification accuracy={:6.4f}'.format(total_acc/number_of_objects))