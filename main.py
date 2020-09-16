import math
import sys
import Parser as prs
import PrePro as pp

code = sys.argv[1]
filtered = pp.PrePro.filter(code)
node = prs.Parser.run(filtered)
final = node.Evaluate()
print(final)

