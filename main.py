import math
import sys
import Parser as prs
import PrePro as pp
import SymbolTable as st


file = open(sys.argv[1],"r")
code = file.read()
file.close()
filtered = pp.PrePro.filter(code)
symbolTable = st.SymbolTable()
node = prs.Parser.run(filtered)
node.Evaluate(symbolTable)


