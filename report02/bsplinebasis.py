from matplotlib import pyplot as plt
import numpy as np

global K
order = int(input("Input the order of B-spline function -> "))#次元数の入力
knot = [0, 1, 1.000000001,2,  3, 4, 5, 6]
#knot = list(map(int, input().split()))   # knotの入力
K = len(knot)

def basis(n, knot, i, u):
    global K
    if n > 0:
        if knot[i] <= u < knot[i+n+1]:
            return (u-knot[i])*basis(n-1,knot,i,u)/(knot[min(i+n, K-1)]-knot[i])\
                +(knot[min(i+n+1, K-1)]-u)*basis(n-1,knot,min(i+1, K-1),u)/(knot[min(i+n+1, K-1)]-knot[min(i+1, K-1)])
        else:
            return 0
    if n == 0:
        if knot[i] <= u < knot[min(i+1, K-1)]:   
            return 1
        else:
            return 0

s, e = knot[0], knot[-1]

for i in range(K-order-1):
    x = []
    y = []
    for j in np.arange(s-2, e+3, 1/100):
        x.append(j)
        y.append(basis(order, knot, i, j))
    plt.plot(x, y)

plt.show()
