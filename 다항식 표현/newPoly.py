import numpy as np
import sympy as sym
import csv
import time

def graphTopoly(vertex, colorBit):
  varCount = vertex * colorBit
  varNames = []
  varObjexts = []
  edgeList = []
  st = time.time()
  
  # make variables
  for i in range(varCount):
    varNames.append('var' + str(i))
    varObjexts.append(sym.symbols(varNames[i]))
  weight = sym.symbols('w')
  
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
  f.close()
  
  # 최종 식 생성
  fin_poly = edgeList[0]
  for i in edgeList[1:]:
    fin_poly += i
  poly='+w*(0'
  for ver in range(0,vertex):
    for color in range(0,colorBit):
      poly+=f'+{2**color}*{varNames[ver*colorBit+color]}'
  poly+=')'
  fin_poly += sym.sympify(poly)
  print('식 생성 완료')
  
  # 결과 값 출력
  CostList = list(200 for ele in range(10))
  ColorList = list(0 for ele in range(10))
  maxCost = 200
  for i in np.ndindex(tuple(2 for j in range(varCount))):
    poly = fin_poly
    a = list(ele for ele in zip(varObjexts, i))
    a.append((weight, 0.01))
    answer = poly.subs(a)
    if answer < 1 and answer<maxCost:
      InsertIndex = 0
      for x in range(10):
        if answer > CostList[x]:
          InsertIndex += 1
      if(InsertIndex == 10):
        maxCost = answer
      CostList.insert(InsertIndex, answer)
      ColorList.insert(InsertIndex, i)
      del CostList[10]
      del ColorList[10]
  print("계산 끝! 파일 출력 시작")
  result = open('다항식 표현\\result.txt', 'w', encoding='utf-8')
  result.write(f'정점:{vertex}개, 실행 시간:{time.time()-st}초' +'\n')
  ui = ''
  for i in range(0, vertex):
    ui += f'V{str(i):<4}'
  ui += 'cost'
  result.write(ui + '\n' + ('_'*len(ui)) + '\n')
  for j in range(len(ColorList)):
    ui = ''
    for ver in range(vertex):
      Total = 0
      for bit in range(colorBit):
        Total += ColorList[j][ver*colorBit + bit] * 2**bit
      ui += f'{Total:<5}'
    result.write(f'{ui}Cost:{CostList[j]}\n')
  result.close()
  print('done')
  return None

graphTopoly(5, 3)