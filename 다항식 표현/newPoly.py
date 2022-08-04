import numpy as np
from sympy import *
import csv
import time
import math

def is_Number(x):
  try:
    a = float(x)
    return True
  except:
    return False

def graphTopoly(vertex, colorBit):
  varCount = vertex * colorBit
  varNames = []
  varObjexts = []
  edgeList = []
  st = time.time()
  
  # make variables
  for i in range(varCount):
    varNames.append('var' + str(i))
    varObjexts.append(symbols(varNames[i]))
  
  # load graph
  f = open('다항식 표현\data.csv', 'r', encoding='utf-8')
  rdr = list(csv.reader(f))
  for y in range(0, vertex):
    for x in range(y, vertex):
      if rdr[y][x].strip() == '1':
        poly = '1'
        for i in range(colorBit):
          poly+= f'*(2*{varNames[x*colorBit+i]}*{varNames[y*colorBit+i]}-{varNames[x*colorBit+i]}-{varNames[y*colorBit+i]}+1)'
        edgeList.append(sympify(poly))
  f.close()
  
  # 최종 식 생성
  not_qubo_poly = edgeList[0]
  for i in edgeList[1:]:
    not_qubo_poly += i
  print(not_qubo_poly.expand())
  poly='-0.01*(0'
  for ver in range(0,vertex):
    for color in range(0,colorBit):
      poly+=f'+{2**color}*{varNames[ver*colorBit+color]}'
  poly+=')'
  not_qubo_poly += sympify(poly)
  
  # degree reduction
  qubo_poly = ''
  extra_var_list = []
  extra_var_name = []
  polys = str(not_qubo_poly.expand()).split(' ')
  for i in range(0, len(polys),2):
    if polys[i].count('var') > 2:
      # 필요함
      if i != 0:
        if polys[i-1] == '-':
          # freedman method
          extra_var_name.append(f'w{len(extra_var_list)}')
          extra_var_list.append(symbols(extra_var_name[-1]))
          abcdefg = polys[i].split('*')
          if(is_Number(abcdefg[0])):
            qubo_poly += f'+{abcdefg[0]}*{extra_var_name[-1]}*({polys[i].count("var")-1}'
            for j in range(1, len(abcdefg)):
              qubo_poly += f'-{abcdefg[j]}'
          else:
            qubo_poly += f'+{extra_var_name[-1]}*({polys[i].count("var")-1}'
            for j in range(0, len(abcdefg)):
              qubo_poly += f'-{abcdefg[j]}'
          qubo_poly += ')'
        else:
          # Ishikawa method
          if polys[i].count('var') % 2 == 0:
            abcdefg = polys[i].split('*')
            k = math.floor((polys[i].count('var') - 1) / 2)
            d = len(abcdefg)
            varStart = len(extra_var_list)
            for _ in range(k):
              extra_var_name.append(f'w{len(extra_var_list)}')
              extra_var_list.append(symbols(extra_var_name[-1]))
            if(is_Number(abcdefg[0])):
              qubo_poly += f'+{abcdefg[0]}*(0'
              for n1 in range(1,d):
                for n2 in range(n1+1, d):
                  qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
              for n1 in range(k):
                qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
              for n1 in range(k):
                for n2 in range(d-1):
                  qubo_poly += f'-2*{abcdefg[1+n2]}*{extra_var_name[varStart + n1]}'
              qubo_poly += ')'
            else:
              qubo_poly += f'+(0'
              for n1 in range(d):
                for n2 in range(n1+1, d):
                  qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
              for n1 in range(k):
                qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
              for n1 in range(k):
                for n2 in range(d):
                  qubo_poly += f'-2*{abcdefg[n2]}*{extra_var_name[varStart + n1]}'
              qubo_poly += ')'
          else:
            abcdefg = polys[i].split('*')
            k = math.floor((polys[i].count('var') - 1) / 2)
            d = len(abcdefg)
            varStart = len(extra_var_list)
            for _ in range(k):
              extra_var_name.append(f'w{len(extra_var_list)}')
              extra_var_list.append(symbols(extra_var_name[-1]))
            if(is_Number(abcdefg[0])):
              qubo_poly += f'+{abcdefg[0]}*(0'
              for n1 in range(1,d):
                for n2 in range(n1+1, d):
                  qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
              for n1 in range(k):
                qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
              for n1 in range(k):
                for n2 in range(d-1):
                  qubo_poly += f'-2*{abcdefg[n2]}*{extra_var_name[varStart + n1]}'
              qubo_poly += f'+{extra_var_name[varStart + k]}*(0'
              for n1 in range(d-1):
                qubo_poly += f'+{abcdefg[n1]}'
              qubo_poly += f'-{d-1}+1))'
            else:
              qubo_poly += f'+(0'
              for n1 in range(d):
                for n2 in range(n1+1, d):
                  qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
              for n1 in range(k):
                qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
              for n1 in range(k):
                for n2 in range(d):
                  qubo_poly += f'-2*{abcdefg[n2]}*{extra_var_name[varStart + n1]}'
              qubo_poly += f'+{extra_var_name[varStart + k]}*(0'
              for n1 in range(d):
                qubo_poly += f'+{abcdefg[n1]}'
              qubo_poly += f'-{d}+1))'
      else:
        # Ishikawa method
        if polys[i].count('var') % 2 == 0:
          abcdefg = polys[i].split('*')
          k = math.floor((polys[i].count('var') - 1) / 2)
          d = len(abcdefg)
          varStart = len(extra_var_list)
          for _ in range(k):
            extra_var_name.append(f'w{len(extra_var_list)}')
            extra_var_list.append(symbols(extra_var_name[-1]))
          if(is_Number(abcdefg[0])):
            qubo_poly += f'+{abcdefg[0]}*(0'
            for n1 in range(1,d):
              for n2 in range(n1+1, d):
                qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
            for n1 in range(k):
              qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
            for n1 in range(k):
              for n2 in range(d-1):
                qubo_poly += f'-2*{abcdefg[1+n2]}*{extra_var_name[varStart + n1]}'
            qubo_poly += ')'
          else:
            qubo_poly += f'+(0'
            for n1 in range(d):
              for n2 in range(n1+1, d):
                qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
            for n1 in range(k):
              qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
            for n1 in range(k):
              for n2 in range(d):
                qubo_poly += f'-2*{abcdefg[n2]}*{extra_var_name[varStart + n1]}'
            qubo_poly += ')'
        else:
          abcdefg = polys[i].split('*')
          k = math.floor((polys[i].count('var') - 1) / 2)
          d = len(abcdefg)
          varStart = len(extra_var_list)
          for _ in range(k):
            extra_var_name.append(f'w{len(extra_var_list)}')
            extra_var_list.append(symbols(extra_var_name[-1]))
          if(is_Number(abcdefg[0])):
            qubo_poly += f'+{abcdefg[0]}*(0'
            for n1 in range(1,d):
              for n2 in range(n1+1, d):
                qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
            for n1 in range(k):
              qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
            for n1 in range(k):
              for n2 in range(d-1):
                qubo_poly += f'-2*{abcdefg[n2]}*{extra_var_name[varStart + n1]}'
            qubo_poly += f'+{extra_var_name[varStart + k]}*(0'
            for n1 in range(d-1):
              qubo_poly += f'+{abcdefg[n1]}'
            qubo_poly += f'-{d-1}+1))'
          else:
            qubo_poly += f'+(0'
            for n1 in range(d):
              for n2 in range(n1+1, d):
                qubo_poly += f'+{abcdefg[n1]}*{abcdefg[n2]}'
            for n1 in range(k):
              qubo_poly += f'+{n1 * 4 - 1}*{extra_var_name[varStart + n1]}'
            for n1 in range(k):
              for n2 in range(d):
                qubo_poly += f'-2*{abcdefg[n2]}*{extra_var_name[varStart + n1]}'
            qubo_poly += f'+{extra_var_name[varStart + k]}*(0'
            for n1 in range(d):
              qubo_poly += f'+{abcdefg[n1]}'
            qubo_poly += f'-{d}+1))'
    else:
      if i != 0:
        qubo_poly += polys[i-1]
      qubo_poly += polys[i]
  qubo_poly = sympify(qubo_poly)
  print(f'식 생성 완료, 총 변수 {varCount + len(extra_var_list)}개\n{qubo_poly}')
  
  show_count = 10
  CostList = list(200 for _ in range(show_count))
  ColorList = list(0 for _ in range(show_count))
  maxCost = 200
  for i in np.ndindex(tuple(2 for j in range(varCount+len(extra_var_list)))):
    a = list(ele for ele in zip(varObjexts, i))
    for j in range(len(extra_var_list)):
      a.append((extra_var_list[j], i[j]))
    answer = qubo_poly.subs(a)
    if answer<maxCost:
      InsertIndex = 0
      for x in range(show_count):
        if answer > CostList[x]:
          InsertIndex += 1
      if(InsertIndex == show_count):
        maxCost = answer
      else:
        if not(CostList[InsertIndex] == answer and ColorList[InsertIndex] == i[:varCount]):
          CostList.insert(InsertIndex, answer)
          ColorList.insert(InsertIndex, i[:varCount])
          del CostList[show_count]
          del ColorList[show_count]
  print("계산 끝! 파일 출력 시작")
  # 결과 값 출력
  result = open('다항식 표현\\result_test.txt', 'w', encoding='utf-8')
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


graphTopoly(3, 2)