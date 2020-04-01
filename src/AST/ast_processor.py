from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from AST.JavaLexer  import JavaLexer
from AST.JavaParser import JavaParser
from pprint import pformat


class AstProcessor:

    def __init__(self, listener):
        self.listener = listener    
        
    
    # ★ポイント２
    def execute(self, input_source):
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        walker = ParseTreeWalker()
        walker.walk(self.listener, parser.compilationUnit())
        return self.listener.ast_info