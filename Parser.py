import Node as n
import Tokenizer as tkr


class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        current = Parser.tokens.actual

        while (current.type == "PLUS" or current.type == "MINUS" or current.type == "OR") and current.type != "EOF":

            if current.type == "PLUS":
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = n.BinOp("PLUS", [node, term])

            elif current.type == "MINUS":
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = n.BinOp("MINUS", [node, term])

            elif current.type == "OR":
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = n.BinOp("OR", [node, term])
            
            current = Parser.tokens.actual

        return node

    @staticmethod
    def parseRelExpression():
        node = Parser.parseExpression()
        current = Parser.tokens.actual

        while (current.type == "GREATER" or current.type == "LESS" or current.type == "EQUALS") and current.type != "EOF":

            if current.type == "GREATER":
                Parser.tokens.selectNext()
                exp = Parser.parseExpression()
                node = n.BinOp("GREATER", [node, exp])

            elif current.type == "LESS":
                Parser.tokens.selectNext()
                exp = Parser.parseExpression()
                node = n.BinOp("LESS", [node, exp])

            elif current.type == "EQUALS":
                Parser.tokens.selectNext()
                exp = Parser.parseExpression()
                node = n.BinOp("EQUALS", [node, exp])

            current = Parser.tokens.actual

        return node

    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        current = Parser.tokens.actual

        while (current.type == "TIMES" or current.type == "DIVIDED" or current.type == "AND") and current.type != "EOF":

            if current.type == "TIMES":
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = n.BinOp("TIMES", [node, factor])

            elif current.type == "DIVIDED":
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = n.BinOp("DIVIDED", [node, factor])

            elif current.type == "AND":
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = n.BinOp("AND", [node, factor])
            
            current = Parser.tokens.actual

        return node

    @staticmethod
    def parseFactor():
        current = Parser.tokens.actual
        # print(current.value)

        if current.type == "PLUS":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = n.UnOp("PLUS", [factor])

        elif current.type == "MINUS":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = n.UnOp("MINUS", [factor])

        elif current.type == "INT":
            node = n.IntVal(current.value)
            Parser.tokens.selectNext()

        elif current.type == "BOOL":
            if current.value == "true":
                node = n.BoolVal(True)
            else:
                node = n.BoolVal(False)
            Parser.tokens.selectNext()

        elif current.type == "STRING":
            node = n.StringVal(current.value)
            Parser.tokens.selectNext()

        elif current.type == "OPEN":
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()
            current = Parser.tokens.actual
            if current.type != "CLOSE":
                raise Exception("Nao fechou parenteses")
            Parser.tokens.selectNext()

        elif current.type == "VARIABLE":
            Parser.tokens.selectNext()
            node = n.Identifier(current.value)

        elif current.type == "NOT":
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = n.UnOp("NOT", [factor])

        else:
            raise Exception("Queria FACTOR, recebeu {}".format(current.type))

        return node
            
    @staticmethod
    def parseCommand():
        current = Parser.tokens.actual

        if current.type == "VARIABLE":
            var = n.Identifier(current.value)
            Parser.tokens.selectNext()
            current = Parser.tokens.actual

            if current.type == "ASSIGNMENT":
                Parser.tokens.selectNext()
                current = Parser.tokens.actual

                if current.value == "readline":
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual

                    if current.type == "OPEN":
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual

                        if current.type == "CLOSE":
                            Parser.tokens.selectNext()
                            nRead = n.ReadLine()
                            node = n.Assignment("ASSIGNMENT", [var, nRead])
                            current = Parser.tokens.actual

                        else:
                            raise Exception(
                                "Queria CLOSE, recebeu {}".format(current.type))
                    else:
                        raise Exception(
                            "Queria OPEN, recebeu {}".format(current.type))

                else:
                    exp = Parser.parseRelExpression()
                    node = n.Assignment("ASSIGNMENT", [var, exp])
                    current = Parser.tokens.actual

                if current.type == "ENDLINE":
                    Parser.tokens.selectNext()

                    return node

                else:
                    raise Exception(
                        "Queria ENDLINE, recebeu {}".format(current.type))
            else:
                raise Exception(
                    "Queria ASSIGNMENT, recebeu {}".format(current.type))

        elif current.type == "RESERVED":

            if current.value == "println":
                Parser.tokens.selectNext()
                current = Parser.tokens.actual

                if current.type == "OPEN":
                    Parser.tokens.selectNext()
                    exp = Parser.parseRelExpression()
                    node = n.Println("PRINT", [exp])
                    current = Parser.tokens.actual

                    if current.type == "CLOSE":
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual

                        if current.type == "ENDLINE":
                            Parser.tokens.selectNext()

                            return node

                        else:
                            raise Exception(
                                "Queria ENDLINE, recebeu {}".format(current.type))
                    else:
                        raise Exception(
                            "Queria CLOSE, recebeu {}".format(current.type))
                else:
                    raise Exception(
                        "Queria OPEN, recebeu {}".format(current.type))

            elif current.value == "if":
                Parser.tokens.selectNext()
                relExp = Parser.parseRelExpression()
                nodeIf = n.If("IF", [relExp])
                current = Parser.tokens.actual

                if current.type == "ENDLINE":
                    Parser.tokens.selectNext()
                    blockIf = Parser.parseBlock()
                    nodeIf.children.append(blockIf)
                    current = Parser.tokens.actual
                    listElseIf = []

                    if current.value == "elseif":

                        while current.value == "elseif":
                            Parser.tokens.selectNext()
                            relExp = Parser.parseRelExpression()
                            nodeElseIf = n.If("ELSEIF", [relExp])
                            current = Parser.tokens.actual

                            if current.type == "ENDLINE":
                                Parser.tokens.selectNext()
                                blockElseIf = Parser.parseBlock()
                                nodeElseIf.children.append(blockElseIf)
                                listElseIf.append(nodeElseIf)
                                current = Parser.tokens.actual
                            
                            else:
                                raise Exception(
                                    "Queria ENDLINE, recebeu {}".format(current.type))

                        if current.value == "else":
                            Parser.tokens.selectNext()
                            current = Parser.tokens.actual
                
                            if current.type == "ENDLINE":
                                Parser.tokens.selectNext()
                                blockElse = Parser.parseBlock()
                                listElseIf[-1].children.append(blockElse)

                            else:
                                raise Exception(
                                    "Queria ENDLINE, recebeu {}".format(current.type))
                        elseIfRange = range(1,len(listElseIf))
                        elseIfRange = reversed(elseIfRange)
                        for i in elseIfRange:
                            listElseIf[i-1].children.append(listElseIf[i])

                        nodeIf.children.append(listElseIf[0])

                    elif current.value == "else":
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual
                        
                        if current.type == "ENDLINE":
                            Parser.tokens.selectNext()
                            blockElse = Parser.parseBlock()
                            nodeIf.children.append(blockElse)

                        else:
                            raise Exception(
                                "Queria ENDLINE, recebeu {}".format(current.type))

                    current = Parser.tokens.actual

                    if current.value == "end":
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual

                        if current.type == "ENDLINE":
                            Parser.tokens.selectNext()

                            return nodeIf

                        else:
                            raise Exception(
                                "Queria ENDLINE, recebeu {}".format(current.type))

                    else:
                        raise Exception(
                            "Queria end, recebeu {}".format(current.value))

                else:
                    raise Exception(
                        "Queria ENDLINE, recebeu {}".format(current.type))

            elif current.value == "while":
                Parser.tokens.selectNext()
                relExp = Parser.parseRelExpression()
                node = n.While("WHILE", [relExp])
                current = Parser.tokens.actual

                if (current.type == "ENDLINE"):
                    Parser.tokens.selectNext()
                    blockWhile = Parser.parseBlock()
                    node.children.append(blockWhile)
                    current = Parser.tokens.actual

                    if current.value == "end":
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual

                        if current.type == "ENDLINE":
                            Parser.tokens.selectNext()
                            return node

                        else:
                            raise Exception(
                                "Queria ENDLINE, recebeu {}".format(current.type))

                    else:
                        raise Exception(
                            "Queria end, recebeu {}".format(current.type))

                else:
                    raise Exception(
                        "Queria ENDLINE, recebeu {}".format(current.value))
                
            elif current.value == "local":
                Parser.tokens.selectNext()
                current = Parser.tokens.actual
                if current.type == "VARIABLE":
                    var = n.Identifier(current.value)
                    Parser.tokens.selectNext()
                    current = Parser.tokens.actual
                    if current.type == "DECLARE":
                        Parser.tokens.selectNext()
                        current = Parser.tokens.actual
                        if current.type == "TYPE":
                            varType = n.Type(current.value)
                            node = n.DeclareVar("DECVAR", [var, varType])
                            Parser.tokens.selectNext()
                            current = Parser.tokens.actual
                            if current.type == "ENDLINE":
                                Parser.tokens.selectNext()
                                return node


        elif (current.type == "ENDLINE"):
            Parser.tokens.selectNext()

            return n.NoOp()

        else:
            raise Exception(
                "Queria ENDLINE - final, recebeu {}".format(current.type))

    @staticmethod
    def parseBlock():
        current = Parser.tokens.actual
        statements = n.Statements()
        while (current.value != "end" and current.type != "EOF" and current.value != "else" and current.value != "elseif"):
            command = Parser.parseCommand()
            statements.children.append(command)
            current = Parser.tokens.actual
            # print(current.type)
        return statements

    @staticmethod
    def run(code):
        Parser.tokens = tkr.Tokenizer(code)
        Parser.tokens.selectNext()
        node = Parser.parseBlock()
        current = Parser.tokens.actual
        if current.type == "EOF":
            return node
        else:
            raise Exception("Tokenizer nao chegou no EOF")
