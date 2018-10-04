import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Input ASM program file name.")
args = parser.parse_args()

input_file = args.filename
out_file_path = "./" + args.filename 
out_file = open(out_file_path + ".out", "w+")
# input_file = "./PROBLEMA3"
# out_file_path = "./program.out"
# out_file = open(out_file_path, "w+")
program = []
data = []
labels = {} # Holds tags and where they are located
memory = {}
ts = r'[ \t,]+' # Token separation pattern

def emptyLine(l):
    """ Returns True if the line is composed of empty tokens (e.g. ['', '']) """
    total = 0
    for e in l:
        total += len(e)
    return total == 0

def validOperand(operand: str):
    """ Checks if operand is a valid integer OR a valid label 
        Returns True/False"""
    if operand.isnumeric():
        if int(operand) > 255:
            print("Integer out of range: ", end='')  
            return (False, 0)                                                   # Is a number
        return (True, "Lit")
    elif operand in labels.keys() or operand in memory.keys():                  # Is a label or memory
        return (True, "Dir")
    elif operand[0] == '#':
        if int (operand[1:], 16) > 255:
            print("Integer out of range: ", end='')  
            return (False, 0) 
        return (True, "Lit")
    elif len(operand) >= 3:
        if operand[1:-1].isnumeric():                                           # Is a (number) 
            if int(operand[1:-1]) > 255:
                print("Integer out of range: ", end='')
                return (False, 0)          
            return (True, "(B)")
        elif operand[1:-1] in labels.keys() or operand[1:-1] in memory.keys():  # Is a (Dir)
            return (True, "(Dir)")
    return (False, 0)

def int2BinaryString(number, lenght):
    if number[0] == '(':
        number = number[1:-1]
    elif number[0] == '#':
        number = str(int(number[1:], 16))
    if memory.__contains__(number):
        number = memory[number]
    elif labels.__contains__(number):
        number = labels[number]
    return ('0'*(lenght-len(bin(int(number))[2:])) if (lenght-len(bin(int(number))[2:])) > 0 else "") + bin(int(number))[2:]

'''Part 1:  Remove comments, empty lines and build program list '''

original_lines_count = 0
with open(input_file, 'r') as file:
    code = False
    for line in file:
        code = False if re.match(r'CODE', line) == None and not code else True
        line = re.sub(r'\n', r'', line)    # Remove newline character
        line = re.sub(r' \/\/.*', r'', line)  # Remove comments
        line.rstrip()
        line_tokens = [i for i in re.split(ts ,line)]
        # print(line_tokens)
        if not code:
            data.append(line_tokens)  # For now, skip DATA section
        elif not emptyLine(line_tokens):
            # print(line_tokens)
            program.append(line_tokens)
        original_lines_count += 1
''' Part 2: Create labels dictionary '''

program = program[1:] # Remove ['CODE:']
for i in range(len(program)):
    if re.match(r'[a-z_A-Z0-9]+\:$', program[i][0]) != None:   # if the first token in line is smthg like "word:"
        labels[program[i][0][:-1]] = i                  # save that token, minus ":", and its line number

''' Part 3: Create memory dictionary '''

data = data[1:]
for i in range(len(data)):
    if re.match(r'[a-zA-Z0-9_]+$', data[i][0]) != None:   # if the first token in line is smthg like "word:"
        memory[data[i][0]] = i  

''' Part 3.1: Create .mem file '''
if (len(memory.items()) > 0):
    out_mem = open(out_file_path+".mem", "w+")
    for item in data:
        print(int2BinaryString(str(item[1]) if item[1].isnumeric() else '0', 8), file=out_mem)
    out_mem.close() 

''' Part 4: Translate opcodes '''

opcodes = {"MOV":{"A":      {"B":"0000000", "Lit":"0000010", "(Dir)": "0100101", "(B)":"0101001"},
                  "B":      {"A":"0000001", "Lit":"0000011", "(Dir)": "0100110", "(B)":"0101010"},
                  "(Dir)":  {"A":"0100111", "B":"0101000"},
                  "(B)":    {"A": "0101011"}},
           "ADD":{"A":      {"B":"0000100", "Lit":"0000110", "(Dir)": "0101100", "(B)":"0101110"},
                  "B":      {"A":"0000101", "Lit":"0000111", "(Dir)": "0101101"},
                  "(Dir)":  "0101111"},
           "SUB":{"A":      {"B":"0001000", "Lit":"0001010", "(Dir)": "0110000", "(B)":"0110010"},
                  "B":      {"A":"0001001", "Lit":"0001011", "(Dir)": "0110001"},
                  "(Dir)":  "0110011"},
           "AND":{"A":      {"B":"0001100", "Lit":"0001110", "(Dir)": "0110100", "(B)": "0110110"},
                  "B":      {"A":"0001101", "Lit":"0001111", "(Dir)": "0110101"},
                  "(Dir)":  "0110111"},
           "OR" :{"A":      {"B":"0010000", "Lit":"0010010", "(Dir)": "0111000", "(B)": "0111010"},
                  "B":      {"A":"0010001", "Lit":"0010011", "(Dir)": "0111001"},
                  "(Dir)":  "0111011"},
           "NOT":{"A":      {"B":"0010100", "A":"0010101"},
                  "B":      {"A":"0010110", "B":"0010111"},
                  "(Dir)":  {"A": "0111100", "B": "0111101"},
                  "(B)":    {"": "0111110"}},
           "XOR":{"A":      {"B":"0011000", "Lit":"0011010", "(Dir)": "0111111", "(B)": "1000001"},
                  "B":      {"A":"0011001", "Lit":"0011011", "(Dir)": "1000000"},
                  "(Dir)":  "1000010"},
           "SHL":{"A":      {"B":"0011100", "A":"0011101"},
                  "B":      {"A":"0011110", "B":"0011111"},
                  "(Dir)":  {"A":"1000011", "B":"1000100"},
                  "(B)":    "1000101"},
           "SHR":{"A":      {"B":"0100000", "A":"0100001"},
                  "B":      {"A":"0100010", "B":"0100011"},
                  "(Dir)":  {"A":"1000110", "B":"1000111"},
                  "(B)":    "1001000"},
           "INC":{"B":      "0100100",
                  "(Dir)":  "1001001",
                  "(B)":    "1001010"},
           "RST":{"(Dir)":  "1001011",
                  "(B)":    "1001100"},
           "CMP":{"A":      {"B":"1001101", "Lit":"1001110", "(Dir)":"1010000", "(B)":"1010010"},
                  "B":      {"Lit":"1001111","(Dir)":"1010001"}},
           "JMP":{"Dir":    "1010011"},
           "JEQ":{"Dir":    "1010100"},
           "JNE":{"Dir":    "1010101"},
           "JGT":{"Dir":    "1010110"},
           "JLT":{"Dir":    "1010111"},
           "JGE":{"Dir":    "1011000"},
           "JLE":{"Dir":    "1011001"},
           "JCR":{"Dir":    "1011010"},
           "JOV":{"Dir":    "1011011"},
           "CALL":{"Dir"    "1011100"},
           "RET":{0:       "1011101\n1111101"}, # has to print 2 opcodes
           "PUSH":{"A":     "1011110",
                   "B":     "1011111"},
           "POP":{"A":      "1100000\n1111110",
                  "B":      "1100001\n1111111"},
           "POP2":{"B":      "1100001"}
          }
line_count = 1
output_line_count = 0
errors = 0
for line in program:
    if len(line) > 1:
        if opcodes.__contains__(line[1]):
            if opcodes[line[1]].__contains__(line[2]):
                if line[1] == 'PUSH':
                    if opcodes[line[1]].__contains__(line[2]):
                        print(opcodes[line[1]][line[2]], file=out_file)
                        output_line_count += 1
                    else:
                        print('Error in line %d, %s %s no es válido' % (line_count, line[1], line[2]))
                elif line[1] == 'POP':
                    if opcodes[line[1]].__contains__(line[2]):
                        print(opcodes[line[1]][line[2]], file=out_file)
                        output_line_count += 2
                    else:
                        print('Error in line %d, %s %s no es válido' % (line_count, line[1], line[2]))
                elif line[1] == 'RET':
                    print(opcodes[line[1]][0], file=out_file)
                    output_line_count += 2
                elif opcodes[line[1]][line[2]].__contains__(line[3]):
                    print(opcodes[line[1]][line[2]][line[3]],
                         int2BinaryString(line[3], 8) if validOperand(line[3])[0] else '', file=out_file)
                    output_line_count += 1
                elif validOperand(line[3])[0]:
                    print(opcodes[line[1]][line[2]][validOperand(line[3])[1]],
                          int2BinaryString(line[3], 8) if validOperand(line[3])[0] else '', file=out_file)
                    output_line_count += 1
                else:
                    print('Error in line %d, %s %s %s no es válido' % (line_count, line[1], line[2], line[3]))
                    errors += 1
            elif validOperand(line[2])[0]:
                if len(line) > 3: # Is something like 'label: MOV (Dir) A'
                    if opcodes[line[1]][validOperand(line[2])[1]].__contains__(line[3]):
                        print(opcodes[line[1]][validOperand(line[2])[1]][line[3]],
                         int2BinaryString(line[2], 8) if validOperand(line[2])[0] else '', file=out_file)
                        output_line_count += 1
                    else: # Exists?
                        print(opcodes[line[1]][validOperand(line[2])[1]][validOperand(line[3])[1]],
                              int2BinaryString(line[3], 8) if validOperand(line[3])[0] else '', file=out_file)
                        output_line_count += 1
                else: # Is something like 'label: XOR (Dir)'
                    print(opcodes[line[1]][validOperand(line[2])[1]],
                          int2BinaryString(line[2], 8) if validOperand(line[2])[0] else '', file=out_file)
                    output_line_count += 1

            else:
                print('Error in line %d, %s %s no es válido' % (line_count, line[1], line[2]))
                errors += 1
        else:
            print('Error in line %d, %s no es válido' % (line_count, line[1]))
            errors += 1
    line_count += 1
out_file.close()

if errors > 0: # If there were errors, delete genereted files and exit
    from os import remove
    remove(out_file_path + ".out")
    remove(out_file_path + ".mem")
    exit()

print("# lines original file: " + str(original_lines_count) +
      "\n# lines of code: " + str(line_count) +
      "\n# lines in .out: " + str(output_line_count))
