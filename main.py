import math
import sys
import Parser as prs
import PrePro as pp

code = sys.argv[1]
# print(sys.argv)
# for i in range(1,len(sys.argv)):
#     code += sys.argv[i]
filtered = pp.PrePro.filter(code)
result = prs.Parser.run(filtered)
print(result)

