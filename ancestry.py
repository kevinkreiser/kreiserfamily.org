#!/usr/bin/env python3
import sys

# pretty straight forward we dont do any tree traversal. since the file is already indented to show
# relationships we can simply fuzzy match the text and print the path via indents to that location


# load the text file into memory so we can search it
with open(sys.argv[1], 'r') as f:
    lines = list(f)

# search for the nth occurance of the text
find = sys.argv[2]
occurance = 0
if len(sys.argv) > 3:
    occurance = int(sys.argv[3])
for line_number, line in enumerate(lines):
    if line.find(find) == -1:
        continue
    occurance -= 1
    if occurance < 0:
        break

# nothing
if line_number == len(lines):
    print('not found')
    sys.exit(1)

def indent(line):
    return len(line) - len(line.lstrip())

# loop backwards up the tree printing each branching
ancestors = []
current_indent = len(lines)
while line_number >= 0:
    next_indent = indent(lines[line_number])
    if next_indent < current_indent:
        ancestors.append(lines[line_number])
        current_indent = next_indent
    line_number -= 1

for ancestor in reversed(ancestors):
    print(ancestor.strip())
