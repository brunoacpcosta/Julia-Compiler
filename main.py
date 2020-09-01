import math
import sys
import Parser as prs

#list_test = ["1+2", "3-2", "1+2-3", "11+22-33", "789     +345   -    123"]
code = ""
for i in range(1,len(sys.argv)):
    code += sys.argv[i]
#print(code)
prs.Parser.run(code)

