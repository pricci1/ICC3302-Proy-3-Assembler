import re

input_file = "./program.txt"
temp_file = "./asm.temp"
program = []
output = []
labels = {} # Holds tags and where they are located
ts = r'[ \t,]+'

def emptyLine(l):
    """ Returns True if the line is composed of empty tokens (e.g. ['', '']) """
    total = 0
    for e in l:
        total += len(e)
    return total == 0



'''Part 1:  Remove comments, empty lines and build program list '''

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

''' Part 2: Create labels dictionary '''
program = program[1:] # Remove ['CODE:']
for i in range(len(program)):
    if re.match(r'[a-z]+\:$', program[i][0]) != None:   # if the first token in line is smthg like "word:"
        labels[program[i][0][:-1]] = i                  # save that token, minus ":", and it's line number

''' Part 3: Translate opcodes '''

for line in program:
    if line[2] == "MOV":                                        # MOV
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "ADD":                                      # ADD
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "SUB":                                      # SUB
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "AND":                                      # AND
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "OR":                                      # OR
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "NOT":                                      # NOT
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "XOR":                                      # XOR
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "SHL":                                      # SHL
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "SHR":                                      # SHR
        if line[3] == "A":
            pass
        elif line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    elif line[2] == "INC":                                      # INC
        if line[3] == "B":
            pass
        else:
            print('Error, %s %s no existe',line[2], line[3])
    



