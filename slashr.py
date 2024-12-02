line = 0
variables = []
variabledata = []
from decimal import Decimal
from functools import cache
def reset():
  global line
  global mainsect
  global subsect
  global subsubsect
  mainsect = ""
  subsect = ""
  subsubsect = ""
  line += 1
def parse(text, start, chars):
  i = 0
  returnVal = ""
  while str(text)[start+i] not in chars:
    returnVal += str(text)[start+i]
    i += 1
  return returnVal

@cache
def operatin(one, two, operation, linenum):
  if operation == "*":
    return Decimal(one) * Decimal(two)
  if operation == "+":
    return Decimal(one) + Decimal(two)
  if operation == "-":
    return Decimal(one) - Decimal(two)
  if operation == "|":
    return Decimal(one) / Decimal(two)
  if operation == "%":
    return Decimal(one) % Decimal(two)
  if operation == "^":
    return Decimal(one) % Decimal(two)
  if operation == ">":
    return Decimal(one) > Decimal(two)
  if operation == "<":
    return Decimal(one) < Decimal(two)
  if operation == "=":
    return Decimal(one) == Decimal(two)
  if operation == ">=":
    return Decimal(one) >= Decimal(two)
  if operation == "<=":
    return Decimal(one) <= Decimal(two)
  else:
    print("Error on Line "+str(linenum+1)+": operation not found")
    quit()


charss = ["*", "+", "-", "|", "%", "^", ">", "<", "="]
def math(line, start, linenum):
  global charss
  one = 0
  two = 0
  inc = 0
  operation = ""
  text = parse(line, start, charss)
  leng = len(str(text))
  if text[0] == ":":
    subsect = parse(line, start+1, charss)
    if not subsect in variables:
        print("Error on Line "+str(linenum+1)+": variable not declared")
    one = variabledata[variables.index(subsect)]
    inc = 1
  else:
    one = text
  length = len(str(text))
  text = line[start+length]
  if text not in charss:
    print("Error on Line "+str(linenum+1)+": operation not found")
    quit()
  operation = text
  text = line[start+length+1]
  if text in charss:
    operation += text
    inc += 1
  text = parse(line + "¬", start+1+leng, "¬")
  if text[0] == ":":
    subsect = parse(line+"¬", start+2+leng, "¬")
    if not subsect in variables:
      print("Error on Line "+str(linenum+1)+": variable not declared")
      quit()
    two = variabledata[variables.index(subsect)]
  else:
    two = text
  return operatin(one, two, operation, linenum)

def run(filename):
  cod = open(filename, "r")
  code = cod.readlines()
  global line
  global mainsect
  global subsect
  global subsubsect
  reset()
  line = 0
  length = len(code)
  while line < length:
    mainsect = parse(code[line], 0, list("/"))
    if mainsect == "let":
      subsect = parse(code[line], 4, list("/"))
      if subsect in variables:
        variablenum = variables.index(subsect)
      else:
        variables.append(subsect)
        variabledata.append("")
        variablenum = variables.index(subsect)
      subsect = parse(code[line], 5+len(subsect), list("/"))
      if subsect[0] == "(" and subsect[-1] == ")":
          variabledata[variablenum] = math(subsect[1:-1], 0, line)
      else:
          variabledata[variablenum] = subsect
      reset()
      continue
    elif mainsect == "out":
      subsect = parse(code[line], 4, list("/"))
      if str(subsect)[0] == ":":
        subsect = parse(code[line], 5, list("/"))
        if not subsect in variables:
          print("Error on Line "+str(line+1)+": variable not declared")
          quit()
        subsect = variabledata[variables.index(subsect)]
      print(subsect)
      reset()
      continue
    elif mainsect == "go":
      subsect = parse(code[line], 3, list("/"))
      if str(subsect)[0] == ":":
        subsect = parse(code[line], 4, list("/"))
        if not subsect in variables:
          print("Error on Line "+str(line+1)+": variable not declared")
          quit()
        subsect = variabledata[variables.index(subsect)]
      try:
        int(subsect)
      except:
        print("Error on Line "+str(line+1)+": expected int")
        quit()
      if int(subsect) < 1:
        print("Error on Line "+str(line+1)+": expected value of at least 1")
        quit()
      templine = int(subsect)-1
      if templine >= length:
        print("Error on Line "+str(line+1)+": line doesn't exist")
      line = templine - 1
      reset()
      continue
    elif mainsect == "del":
      subsect = parse(code[line], 4, list("/"))
      if subsect in variables:
        variablenum = variables.index(subsect)
      else:
          print("Error on Line"+str(line+1)+": variable not declared")
      variables.pop(variablenum)
      variabledata.pop(variablenum)
      reset()
      continue
    elif mainsect == "if":
      subsect = parse(code[line], 3, list("/"))
      leng = len(subsect)
      if subsect[0] == "(" and subsect[-1] == ")":
          subsect = math(subsect[1:-1], 0, line)
      try:
        subsect = bool(subsect)
      except:
        print("Error on Line"+str(line+1)+": expected boolean value")
        quit()
      if subsect == False:
        subsect = parse(code[line], 4+leng, list("/"))
        if str(subsect)[0] == ":":
          subsect = parse(code[line], subsect[1:], list("/"))
          if not subsect in variables:
            print("Error on Line "+str(line+1)+": variable not declared")
            quit()
          subsect = variabledata[variables.index(subsect)]
        try:
          int(subsect)
        except:
          print("Error on Line "+str(line+1)+": expected int")
          quit()
        if int(subsect) < 1:
          print("Error on Line "+str(line+1)+": expected value of at least 1")
          quit()
        templine = int(subsect)-1
        if templine >= length:
          print("Error on Line "+str(line+1)+": line doesn't exist")
          quit()
        line = templine - 1
      reset()
      continue
    elif mainsect == "":
      reset()
      continue
    else:
      print("Error on Line "+str(line+1)+": command unknown")
      quit()
run("text.slashr")
