from math import sqrt
#from pprint import pprint
import copy
import pdb
#import numpy.matlib
import numpy as np 
from numpy import linalg as LA
from numpy import array
from numpy import diag
from numpy import dot
from numpy import zeros

def rounding(A, case = -1011):
    rslt = copy.deepcopy(A)
    for i in range(len(A)): 
        for j in range(len(A[i])):
            if case != -1011:
                rslt[i][j] = round(rslt[i][j], case)
            else:
                rslt[i][j] = round(rslt[i][j], 2)
    return rslt

def inititialize(m, n):
    rslt = []
    for i in range(m):
        u = []
        for i in range(n):
            u.append(0)
        rslt.append(u)
    return rslt
#This SVD routine uses numpy library to compute the decomposition. 
#We use this routine in case of confronting 2 scenarios:
#1) when the eignvalues are complex.
#2) when the row rank of the A*A^T (or A^T*A) is less than m-1 (or n-1)
def compSVD(B = 0):
    # define a matrix
    #print(A)
    A = array(B)
    # Singular-value decomposition
    U, s, VT = np.linalg.svd(A)
    # create m x n Sigma matrix
    Sigma = zeros((A.shape[0], A.shape[1]))
    # populate Sigma with n x n diagonal matrix
    if len(B) <= len(B[0]):
        Sigma[:A.shape[0], :A.shape[0]] = diag(s)
    else:
        Sigma[:A.shape[1], :A.shape[1]] = diag(s)
    # reconstruct matrix
    B = U.dot(Sigma.dot(VT))
    return U, Sigma, np.transpose(VT)

def Construct(lst, order):
    A = list()
    b = list()
    row = list()
    elmnt = 1
    for i in range(len(lst[0])):
        for j in range(order + 1):
            if j != 0:
                elmnt = elmnt * lst[0][i]  
            row.append(elmnt)
        A.append(list(row))
        b.append([lst[1][i]])
        elmnt = 1
        row.clear()
    return array(A), array(b)

def PrintPolynm(A):
    A = rounding(A,4)
    s = 'P(X) = '
    for i in range(len(A)):
        s += str(A[i][0])
        if i > 0:
            s += 'x^' + str(i)
        if i != len(A) - 1:
            s += ' + '
    print (s)

def Polynomial(coeffs, inp):
    out = 0
    for i in range(len(coeffs)):
        out = out + coeffs[i][0]*pow(inp,i)
    return out

def Error(lst, coeffs):
    #pdb.set_trace()
    error = 0
    for i in range(len(lst[0])):
        t = Polynomial(coeffs,lst[0][i]) - lst[1][i]
        error = error + pow(t,2)
    return error

def process(inp ,order):
    A, b = Construct(inp,order)
    U, S, V = compSVD(A)
    t = np.transpose(U).dot(b)

    C = t.tolist()
    Sigma = S.tolist()
    Z = inititialize(len(Sigma[0]),1)
    if len(Sigma[0]) >= len(Sigma):
        t = len(Sigma)
    else:
        t = len(Sigma[0])
    for i in range(t):
        if Sigma[i][i] == 0:
            Z[i][0] = 0
        else:   
            Z[i][0] = C[i][0]/Sigma[i][i]
    coeffs = V.dot(array(Z)).tolist()
    PrintPolynm(coeffs)
    err = Error(inp, coeffs)
    print ('and the error is: ' + str(err))

def Case(order):
    bool = True
    rstX = 1
    rstY = 1
    i = 0
    j = 0
    inp = [[],[]]
    while bool:
        if rstX == 1:
            print ('\nNow please type all x_i in a row without any commas (e.g. 3 4 -5.2). Number of spaces between numbers does not matter:')
            a = [float(x) for x in input().split()]
            inp[0] = a
            i = 1
            rstX = 0
        if rstY == 1:
            print ('\nNow please all y_i in a row without any commas (e.g. 3 4 -5.2). Number of spaces between numbers does not matter:')
            b = [float(x) for x in input().split()]
            inp[1] = b
            j = 1
            rstY = 0

        print ("\nThe two columns show x_i and y_i. please Check if they're ok.")
        print (np.transpose(array(inp)))  
        print ("If so, type 1 to start the process. Otherwise please type 2 for editting x_i's (and 3 for y_i's and 4 for both):")
        g = input().split()
        c = int(g[0])
        if c == 1:
            process(inp, order)
            bool = False
        elif c == 2:
            rstX = 1
        elif c == 3:
            rstY = 1
        elif c == 4:
            rstX = 1
            rstY = 1

print ("\n***Note1: At every input prompt, please press ENTER when you finished typing.\n")
print ("***Note2: After you enetered input, unfortunately, you can not use arrow keys to edit e.g. the middle of the input! You have to delete from the end! I recommend copying and pasting\n")
print ("***Note3: At each step, if you want to end the program, enter any English letter to get a ValueError which stops the program.\n")

g = input("Please type the order of the polynomial: ").split() 
order = int(g[0])
g = input("\nIn order to use random x and y, please type 1. Otherwise, type 2: ").split() 
case = int(g[0])
if case == 2:
    Case(order)
elif case == 1:
    g = input("\nEnter the number of x_i and y_i: ").split()
    s = int(g[0])
    a = np.random.rand(s,2)
    print ('\nThe two columns show x_i and y_i: ')
    print (a)
    print ()
    inp = a.tolist()
    process(inp, order)

