import math
import sys
import Parser as prs
import PrePro as pp
import SymbolTable as st
import Compiler as cp


file = open(sys.argv[1],"r")
code = file.read()
file.close()
filtered = pp.PrePro.filter(code)
symbolTable = st.SymbolTable()
compiler = cp.Compiler()
node = prs.Parser.run(filtered)
node.Evaluate(symbolTable, compiler)
compiler.flush()


