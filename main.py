import math
import sys
import Parser as prs

code = ""

for i in range(1,len(sys.argv)):
    code += sys.argv[i]
result = prs.Parser.run(code)
print(result)

