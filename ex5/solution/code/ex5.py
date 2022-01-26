import sys

import numpy as np
import math

global powers,p,g

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1

        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1


def q1(m, x):
    t = int(math.sqrt(2 * m))
    rng = np.random.default_rng()
    elements = rng.choice(m, t,replace=False)
    elements.sort()

    # t times
    for i in range(len(elements)):
        q = elements[i] + x

        if q >= m:
            q=-m
            arr= elements[:i]
        else:
            arr = elements[i:]

        if binary_search(arr,q) != -1:
            return [elements[i], q]

    return [None,None]

# assume g^a=g^b * X
# g is generator of cyclic group of size m.
# need to compute the dlog of X in base g.
# X=g^a * (g^b)^-1 =g^(a-b)
# log_g_X=a-b
def q2(a, b,m):
    sub = a-b
    if sub <0:
        sub = (sub%m)-1
    return sub


def q1_alt(p, X):
    t = int(math.sqrt(2 * p))

    rng = np.random.default_rng()
    elements_powers = rng.choice(p-1, t,replace=False)+1
    # if a is a random element then so is g^a
    repeated_squaring_vectorized = np.vectorize(repeated_squaring)
    elements = repeated_squaring_vectorized(elements_powers)
    elements_powers = elements_powers[np.argsort(elements)]
    elements.sort()
    for i in range(t):
        q = (int(elements[i]) * X) % p

        j = binary_search(elements,q)
        if j != -1:
            return [elements_powers[i], elements_powers[j]]

    return [None,None]


# p is prime, g is a generator of Zp*
# need to find log_g_x
def q3(m, base, x):
    global powers,p,g
    p=m
    g=base
    powers = np.zeros(p)
    powers[0]=1
    powers[1]=g

    arr = [None,None]
    while arr[0] is None:
        arr = q1_alt(p,x)
    return q2(arr[1], arr[0],p)


def repeated_squaring(exp):
    a=powers[exp]
    if a ==0:
        t = int(repeated_squaring(exp//2))
        t = int((t*t) % p)
        if exp % 2 == 0:
            a=t
        else:
            a =int((int((g % p)) * t) % p)
        powers[exp]=a
    return a

if __name__ == "__main__":
    print(q3(461733370363, 2, 322893892))