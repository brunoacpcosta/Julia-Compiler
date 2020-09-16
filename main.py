import math
import sys
import Parser as prs
import PrePro as pp


file = open(sys.argv[1],"r")
code = file.read()
file.close()
filtered = pp.PrePro.filter(code)
node = prs.Parser.run(filtered)
final = node.Evaluate()
print(final)

