#Juan Diego Gonzalez German
#1001401837
#11/14/19

import matplotlib as mpl
import numpy as np
import random
import sys

#loading and preparation
data_file = sys.argv[1]
k = int(sys.argv[2])
iterations = int(sys.argv[3])

data = np.loadtxt(data_file)
data_size = data.shape
n = data_size[0]
d = data_size[1] - 1
x = np.delete(data, -1, 1)

#Define Tree
class Gaussian:
    def __init__(self):
        self.w = 0
        self.u = np.zeros(d)
        self.o = np.zeros((d,d))

    def calculateN(self, x):
        subs = np.array([x - self.u])
        t =  np.transpose(subs)
        inv = np.linalg.inv(self.o)
        num = np.exp(-0.5 * np.dot(np.dot(subs,inv),t) )
        den = np.sqrt( np.power(2*np.pi,d) * np.linalg.det(self.o) )
        return float(num/den)

def initialize():
    p = np.zeros((n,k))
    for j in range(n):
        i = random.randint(0, k-1)
        p[j][i] = 1.0
        
    N = []
    for i in range(k):
        N.append(Gaussian())

    return p, N

def MStep(p, N):
    sum_pj = []     #sum of pij for each given i
    for i in range(k):
        curr = 0
        for j in range(n):
            curr += p[j][i]
        sum_pj.append(curr)
    sum_pij = sum(sum_pj) #total sum for pij for all i and j

    for i in range(k):
        Ni = N[i]
        Ni.w = sum_pj[i]/sum_pij

        num = np.zeros(d)
        for j in range(n):
            num += p[j][i]*x[j]
        Ni.u = num/sum_pj[i]

        o = np.zeros((d,d))
        ui = Ni.u
        for r in range(d):
            for c in range(d):
                num = 0
                for j in range(n):
                    xj = x[j]
                    num += p[j][i] * (xj[r]-ui[r]) * (xj[c]-ui[c])
                rc = num/sum_pj[i]
                if r == c and rc < 0.0001:
                    rc = 0.0001
                o[r][c] = rc
        Ni.o = o

def EStep(p, N):
    for j in range(n):
        xj = x[j]
        Nw = []
        for i in range(k):
            Niw = N[i].calculateN(xj) * N[i].w
            Nw.append(Niw)
        Pxj = sum(Nw)
        for i in range(k):
            p[j][i] = Nw[i]/Pxj

def plotClusters(p):
    clusters = [None]*k
    for j in range(n):
        pj = p[j]
        xj = x[j]
        c = np.where(pj == np.amax(pj))[0][0]
        if clusters[c] is None:
            clusters[c] = []
        clusters[c].append(xj)
    for cluster in clusters:
        if cluster is None:
            continue
        xc = [b[0] for b in cluster]
        yc = [b[1] for b in cluster]
        mpl.pyplot.scatter(xc,yc)
    mpl.pyplot.show()
    
p, N = initialize()
#plotClusters(p)
for r in range(iterations):
    MStep(p,N)
    EStep(p,N)
    #plotClusters(p)