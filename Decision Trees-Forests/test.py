import numpy as np
max_class = 3
def distribution(examples):
    count = float(len(examples))
    class_count = [0]*(max_class+1)
    if count == 0:
        return class_count
    for x in examples: 
        class_count[int(x[-1])] += 1
    dist = [x / count for x in class_count]
    return dist

def entropy(dist):
    H = 0
    for x in dist:
        if(x == 0):
            continue
        else:
            H -= x*np.log2(x)
    return H

def infoGain(examples, att, thr):
    dist_n = distribution(examples)
    k_l = list(filter(lambda x: x[att] < thr, examples))
    dist_l = distribution(k_l)
    k_r = list(filter(lambda x: x[att] >= thr, examples))
    dist_r = distribution(k_r)
    print(k_l, k_r)
    print(dist_n, dist_l, dist_r)
    print(entropy(dist_n), entropy(dist_l), entropy(dist_r))
    return entropy(dist_n) - (len(k_l)/float(len(examples))*entropy(dist_l)) - (len(k_r)/float(len(examples))*entropy(dist_r))

even = [[0,0],[1,1]]
#print(infoGain(even,0,1))
odd = [[0,1],[1,1],[2,2],[2,2],[3,3]]
print(infoGain(odd,0,2))

# print('H(200/400,200/400)={:f}'.format(entropy([200/400,200/400])))
# print('H(20/520,500/520)={:f}'.format(entropy([20/520,500/520])))
# print('H(20/5020,5000/5020)={:f}'.format(entropy([20/5020,5000/5020])))
# print('H(0/400,400/400)={:f}'.format(entropy([0/400,400/400])))
# print('H(50/90,15/90,25/90)={:f}'.format(entropy([50/90,15/90,25/90])))

