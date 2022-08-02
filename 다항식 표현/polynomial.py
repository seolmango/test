import numpy as np

def sumTuples(tuple1 : tuple, tuple2 : tuple, length : bool = False) -> tuple:
  """입력된 튜플의 요소들을 각각 더해주는 함수

  Args:
      tuple1 (tuple): 첫번째 튜플
      tuple2 (tuple): 두번째 튜플
      length (bool): 튜플의 요소들에서 각각 1을 뺄지 여부

  Returns:
      tuple: 더한 결과 튜플
  """
  result = []
  if len(tuple1) > len(tuple2):
    a = len(tuple1)-len(tuple2)
    for i in range(a):
      result.append(tuple1[i])
    for i in range(a, len(tuple1)):
      if(length):
        result.append(tuple1[i]+tuple2[i-a]-1)
      else:
        result.append(tuple1[i] + tuple2[i-a])
  else:
    a = len(tuple2)-len(tuple1)
    for i in range(a):
      result.append(tuple2[i])
    for i in range(a, len(tuple2)):
      if(length):
        result.append(tuple2[i]+tuple1[i-a]-1)
      else:
        result.append(tuple1[i-a] + tuple2[i])
  return tuple(result)


class Field():
  
  def __init__(self, dimension : int) -> None:
    """계산을 수행할 때 array의 기본적인 구조를 설정하는 초기화 함수입니다.

    Args:
        dimension (int): 계산 과정에서 사용할 모든 변수의 갯수
    """
    self.dimension = dimension
    
  def graphToPolynomialArray(self, file, colorBit : int) -> np.array:
    """입력된 그래프 파일을 array형태로 변환하는 함수입니다.

    Args:
        file (str): 그래프 파일의 경로
        colorBit (int): 한 정점의 색을 표현하는 데 쓸 이진수의 자릿수
    
    Returns:
        np.array: graph Coloring 완료 되었는지 확인하는 식의 array
    """
    # Load graph
    
  def multiplePolynomial(self, a : np.array, b : np.array) -> np.array:
    """두개의 array로 표현된 다항식을 곱한 결과를 array형태로 반환해주는 함수

    Args:
        a (np.array): 곱할 첫번째 array
        b (np.array): 곱할 두번째 array

    Returns:
        np.array: 곱한 결과 array
    """
    result = np.zeros(sumTuples(a.shape, b.shape, True), int)
    for tempA in np.ndindex(a.shape):
      for tempB in np.ndindex(b.shape):
        result[sumTuples(tempA, tempB)] += a[tempA] * b[tempB]
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
      
a = Field(3)
rowA = [
  [0,1],
  [1,0]
]
rowB = [
  [
    [0,1],
    [1,0]
  ],
  [
    [1,0],
    [0,0]
  ]
]
testA = np.array(rowA)
testB = np.array(rowB)
result = a.multiplePolynomial(testA, testB)
print(result)

      