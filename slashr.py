line = 0
variables = []
variabledata = []
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

charss = ["*", "+", "-", "|", "%"]
def math(line, start):
  global charss
  one = 0
  two = 0
  inc = 0
  operation = ""
  text = parse(line, start, charss)
  if text[0] == ":":
    subsect = parse(line, start+1, charss)
    if not subsect in variables:
        return "variablenotdeclared"
    one = variabledata[variables.index(subsect)]
    inc = 1
  else:
    one = text
    print(one)
  text = line[start+len(str(text))]
  if text not in charss:
    return "operation not found"
  operation = text
  text = parse(line + "¬", start+1+inc+len(str(one)), "¬")
  if text[0] == ":":
    subsect = parse(line+"¬", start+2+inc+len(str(one)), "¬")
    if not subsect in variables:
        return "variablenotdeclared"
    two = variabledata[variables.index(subsect)]
  else:
    two = text
  print(one, two)
  if operation == "*":
    return int(one) * int(two)
  if operation == "+":
    return int(one) + int(two)
  if operation == "-":
    return int(one) - int(two)
  if operation == "|":
    return int(one) / int(two)
  if operation == "%":
    return int(one) % int(two)
  
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
          variabledata[variablenum] = math(subsect[1:-1])
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
    elif mainsect == "if":
      reset()
      continue
    else:
      print("Error on Line "+str(line+1)+": command unknown")
      quit()
run("text.slashr")
