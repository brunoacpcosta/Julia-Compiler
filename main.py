import math
import sys
import Parser as prs
import PrePro as pp

code = sys.argv[1]
filtered = pp.PrePro.filter(code)
result = prs.Parser.run(filtered)
print(result)

