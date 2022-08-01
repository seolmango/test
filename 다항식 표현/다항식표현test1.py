import numpy as np
from traitlets import default

a1 = np.array([[[2,1],[1,0]],[[1,0],[0,0]]],int)
b1 = np.array([[[1,2],[2,3]],[[0,0],[0,0]]],int)
    
def multiplePolynomial(a, b):
  result = np.zeros(tuple(sum(elem)-1 for elem in zip(a.shape, b.shape)), int)
  for tempA in np.ndindex(a.shape):
    for tempB in np.ndindex(b.shape):
      result[tuple(sum(elem) for elem in zip(tempA, tempB))] += a[tempA] * b[tempB]
  return result

# print(multiplePolynomial(a1, b1))

def findmin(array):
  varCom = ()
  nonecheck = ()
  for i in range(array.ndim):
    varCom += (2,)
    nonecheck += (0,)
  for Vartemp in np.ndindex(varCom):
    Comsum = 0
    for Loctemp in np.ndindex(array.shape):
      default_mult = 1
      for j in range(len(Loctemp)):
        if(Loctemp[j] != 0):
          default_mult *= Vartemp[j]
      Comsum += array[Loctemp] * default_mult
    print(Vartemp, " : ", Comsum)
    
min_test = np.array([[[2,1],[1,0]],[[1,0],[0,-1]]],int)
findmin(min_test)