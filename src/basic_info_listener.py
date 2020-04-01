from JavaParserListener import JavaParserListener
from JavaParser import JavaParser

class BasicInfoListener(JavaParserListener):

    def __init__(self):
        self.call_methods = []
        self.ast_info = {
            'imports': [],
            'exception': []
        }

    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        import_class = ctx.qualifiedName().getText()
        self.ast_info['imports'].append(import_class)
    
    def enterMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):

        count = 0
        c = [ctx.getChild(count)] # <-- 子ノードへ遷移
        
        # throwsの単語を探す（Noneが来たら捜索終了）
        while c[0] is not None:
            if c[0] is None:
                break
            #throwsが来た場合、その次の単語を取得する（ファイル名）
            if c[0].getText() == 'throws':
                c2 = ctx.getChild(count+1).getText()
                if '|' in c2:
                    c2_list = c2.split('|')
                    for i in c2_list:
                        self.ast_info['exception'].append(i)
                else:
                    self.ast_info['exception'].append(c2)
            count = count + 1
            c = [ctx.getChild(count)]
            
    # Enter a parse tree produced by JavaParser#catchClause.
    def enterCatchClause(self, ctx:JavaParser.CatchClauseContext):
        catch_type = ctx.catchType().getText()
        if '|' in catch_type:
            catch_type_list = catch_type.split('|')
            for i in catch_type_list:
                self.ast_info['exception'].append(i)
        else:
            self.ast_info['exception'].append(catch_type)

    def enterInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        count = 0
        c = [ctx.getChild(count)] # <-- 子ノードへ遷移
        
        # throwsの単語を探す（Noneが来たら捜索終了）
        while c[0] is not None:
            if c[0] is None:
                break
            #throwsが来た場合、その次の単語を取得する（ファイル名）
            if c[0].getText() == 'throws':
                c2 = ctx.getChild(count+1).getText()
                if '|' in c2:
                    c2_list = c2.split('|')
                    for i in c2_list:
                        self.ast_info['exception'].append(i)
                else:
                    self.ast_info['exception'].append(c2)

            count = count + 1
            c = [ctx.getChild(count)]