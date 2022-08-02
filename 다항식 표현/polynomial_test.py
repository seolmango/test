import numpy as np

def multiplePolynomial(a : np.array, b : np.array) -> np.array:
  """두개의 array로 표현된 다항식을 곱한 결과를 array형태로 반환해주는 함수

  Args:
      a (np.array): 곱할 첫번째 array
      b (np.array): 곱할 두번째 array

  Returns:
      np.array: 곱한 결과 array
  """
  result = np.zeros(tuple(sum(elem)-1 for elem in zip(a.shape, b.shape)), int)
  for tempA in np.ndindex(a.shape):
    for tempB in np.ndindex(b.shape):
      result[tuple(sum(elem) for elem in zip(tempA, tempB))] += a[tempA] * b[tempB]
  return result

def findmin(array : np.array) -> None:
  """입력된 array형태의 다항식의 변수들에 각각 0또는 1일 대입하여 나오는 모든 경우의 결과값을 출력하는 함수

  Args:
      array (np.array): 다항식
  """
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