from AST.JavaParserListener import JavaParserListener
from AST.JavaParser import JavaParser

class BasicInfoListener(JavaParserListener):

    def __init__(self):
        self.call_methods = []
        self.ast_info = {
            'imports': [],
            'exception': [],
            'className': [],
            'implements': [],
            'extends': '',
            'interface':[],
            'interface_extends':[],
            'field_type':[]
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
                elif ',' in c2:
                    c2_list = c2.split(',')
                    for i in c2_list:
                        self.ast_info['exception'].append(i)
                else:
                    self.ast_info['exception'].append(c2)

            count = count + 1
            c = [ctx.getChild(count)]
            
     # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        child_count = int(ctx.getChildCount())
        if child_count == 7:
            # class Foo extends Bar implements Hoge
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            # c3 = ctx.getChild(2)  # ---> extends
            c4 = ctx.getChild(3).getChild(0).getText()  # ---> extends class name
            # c5 = ctx.getChild(4)  # ---> implements
            # c7 = ctx.getChild(6)  # ---> method body
            self.ast_info['className'].append(c2)
            self.ast_info['implements'] = self.parse_implements_block(ctx.getChild(5))
            self.ast_info['extends'] = c4
        elif child_count == 5:
            # class Foo extends Bar
            # or
            # class Foo implements Hoge
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            c3 = ctx.getChild(2).getText()  # ---> extends or implements

            # c5 = ctx.getChild(4)  # ---> method body
            self.ast_info['className'].append(c2)
            if c3 == 'implements':
                self.ast_info['implements'] = self.parse_implements_block(ctx.getChild(3))
            elif c3 == 'extends':
                c4 = ctx.getChild(3).getChild(0).getText()  # ---> extends class name or implements class name
                self.ast_info['extends'] = c4
        elif child_count == 3:
            # class Foo
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            # c3 = ctx.getChild(2)  # ---> method body
            self.ast_info['className'].append(c2)

    def parse_implements_block(self, ctx):
        implements_child_count = int(ctx.getChildCount())
        result = []
        if implements_child_count == 1:
            impl_class = ctx.getChild(0).getText()
            result.append(impl_class)
        elif implements_child_count > 1:
            for i in range(implements_child_count):
                if i % 2 == 0:
                    impl_class = ctx.getChild(i).getText()
                    result.append(impl_class)
        return result

    # Enter a parse tree produced by JavaParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        child_count = int(ctx.getChildCount())
        if child_count <= 3:
            self.ast_info['interface'].append(ctx.getChild(1).getText())
        
        if ctx.getChild(2).getText() == 'extends':
            self.ast_info['interface_extends'].append([ctx.getChild(1).getText(), ctx.getChild(3).getText()])
            self.ast_info['interface'].append(ctx.getChild(1).getText())

    def enterFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        type_list = ['byte','int','short','long','float','double','char','String','boolean','object','byte[]','int[]','short[]','long[]','byte[]','float[]','double[]','char[]','String[]','boolean[]','object[]']
        fieldType = ctx.getChild(0).getText()
        if fieldType not in type_list:
            self.ast_info['field_type'].append(ctx.getChild(0).getText())
