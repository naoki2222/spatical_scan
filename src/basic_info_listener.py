from JavaParserListener import JavaParserListener
from JavaParser import JavaParser


# ★ポイント３
class BasicInfoListener(JavaParserListener):
    

    def __init__(self):
        self.call_methods = []
        self.ast_info = {
            'imports': []
        }

    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        import_class = ctx.qualifiedName().getText()
        self.ast_info['imports'].append(import_class)
