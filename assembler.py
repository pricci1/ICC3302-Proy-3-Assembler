import re

input_file = "./program.txt"
temp_file = "./asm.temp"
program = []
output = []
ts = r'[ \t,]+'

def emptyLine(l):
    """ Returns True if the line is composed of empty tokens (e.g. ['', '']) """
    total = 0
    for e in l:
        total += len(e)
    return total == 0



'''Pass 1:  Remove comments, empty lines '''

with open(input_file, 'r') as file:
    code = False
    for line in file:
        code = False if re.match(r'CODE', line) == None and not code else True
        if not code: continue    # For now, skip DATA section
        
        line = re.sub(r'\n', r'', line)    # Remove newline character
        line = re.sub(r' #.*', r'', line)  # Remove comments
        line_tokens = [i for i in re.split(ts ,line)]
        if not emptyLine(line_tokens):
            print(line_tokens)
            program.append(line_tokens)


      #  print([i for i in re.split(ts ,line) if i != ''])




