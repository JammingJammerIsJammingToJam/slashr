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

def parse(text, start, char):
  i = 0
  returnVal = ""
  while str(text)[start+i] != char:
    returnVal += str(text)[start+i]
    i += 1
  return returnVal

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
    mainsect = parse(code[line], 0, "/")
    if mainsect == "let":
      subsect = parse(code[line], 4, "/")
      if subsect in variables:
        variablenum = variables.index(subsect)
      else:
        variables.append(subsect)
        variabledata.append("")
        variablenum = variables.index(subsect)
      subsect = parse(code[line], 5+len(subsect), "/")
      variabledata[variablenum] = subsect
      reset()
      continue
    elif mainsect == "out":
      subsect = parse(code[line], 4, "/")
      if str(subsect)[0] == ":":
        subsect = parse(code[line], 5, "/")
        if not subsect in variables:
          print("Error on Line "+str(line+1)+": variable not declared")
          quit()
        subsect = variabledata[variables.index(subsect)]
      print(subsect)
      reset()
      continue
    elif mainsect == "go":
      subsect = parse(code[line], 3, "/")
      if str(subsect)[0] == ":":
        subsect = parse(code[line], 4, "/")
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
    elif mainsect == "if":
      reset()
      continue
    else:
      print("Error on Line "+str(line+1)+": command unknown")
      quit()
run("text.slashr")
