import numpy as np
import sympy as sym
import csv

def graphTopoly(vertex, colorBit, colorLimit, onlyAnswer=True):
  varCount = vertex * colorBit
  varNames = []
  varObjexts = []
  edgeList = []
  
  # make variables
  for i in range(varCount):
    varNames.append('var' + str(i))
    varObjexts.append(sym.symbols(varNames[i]))
  
  # load graph
  f = open('다항식 표현\data.csv', 'r', encoding='utf-8')
  rdr = list(csv.reader(f))
  for y in range(0, vertex):
    for x in range(y, vertex):
      if rdr[y][x].strip() == '1':
        poly = '1'
        for i in range(colorBit):
          poly+= f'*(2*{varNames[x*colorBit+i]}*{varNames[y*colorBit+i]}-{varNames[x*colorBit+i]}-{varNames[y*colorBit+i]}+1)'
        edgeList.append(sym.sympify(poly))
  
  # 최종 식 생성
  fin_poly = edgeList[0]
  for i in edgeList[1:]:
    fin_poly += i
  
  result = open('다항식 표현\\result.txt', 'w', encoding='utf-8')
  ui = ''
  for i in range(0, vertex):
    ui += f'V{str(i):<4}'
  ui += 'cost'
  result.write(f'정점:{vertex}개, 최대 {colorLimit}개의 색을 사용' + '\n')
  result.write(ui + '\n' + ('_'*len(ui)) + '\n')
  for i in np.ndindex(tuple(2 for j in range(varCount))):
    poly = fin_poly
    answer = poly.subs(list(ele for ele in zip(varObjexts, i)))
    ComText = ''
    if(onlyAnswer):
      if(int(answer) == 0):
        limit_ = True
        for a in range(vertex):
          djhf = 0
          for b in range(colorBit):
            djhf += i[a*colorBit+b] * 2**b
          ComText += f'{djhf:<5}'
          limit_ = limit_ and (djhf < colorLimit)
        if(limit_):
          result.write(ComText+ str(answer) + "\n")
    else:
      limit_ = True
      for a in range(vertex):
        djhf = 0
        for b in range(colorBit):
          djhf += i[a*colorBit+b] * 2**b
        ComText += f'{djhf:<5}'
        limit_ = limit_ and (djhf < colorLimit)
      if(limit_):
        result.write(ComText + str(answer) + "\n")
  result.close()
  return None

graphTopoly(6, 2, 3, True)