import tkinter as Tk
from collections import OrderedDict


def get_data():

    def load_widget():
        widget_list = list()
        widget_list.append({'type': 'Label', 'text': "リポジトリのURL :", 'relx': 0.01, 'rely': 0.005})
        widget_list.append({'type': 'Entry', 'width': 80, 'relx': 0.11, 'rely': 0.005, 'focus_set': True})
        widget_list.append({'type': 'Label', 'text': "変更前のブランチ :", 'relx': 0.01, 'rely': 0.055})
        widget_list.append({'type': 'Entry', 'width': 20, 'relx': 0.11, 'rely': 0.055})
        widget_list.append({'type': 'Label', 'text': "変更後のブランチ :", 'relx': 0.01, 'rely': 0.105})
        widget_list.append({'type': 'Entry', 'width': 20, 'relx': 0.11, 'rely': 0.105})
        widget_list.append({'type': 'Label', 'text': "クライアントID :", 'relx': 0.01, 'rely': 0.155})
        widget_list.append({'type': 'Entry', 'width': 60, 'relx': 0.11, 'rely': 0.155})
        widget_list.append({'type': 'Label', 'text': "シークレット :", 'relx': 0.01, 'rely': 0.205})
        widget_list.append({'type': 'Entry', 'width': 60, 'relx': 0.11, 'rely': 0.205})
        widget_list.append({'type': 'Button', 'text': "保存", 'relx': 0.11, 'rely': 0.255})
        return widget_list

    def create_widgets(root):

        def func(root):
            global text1
            global text2
            global text3
            global text4
            global text5
            text1 = root.widgets[1].get()
            print("リポジトリのURL : " + text1)
            text2 = root.widgets[3].get()
            print("変更前のブランチ : " +  text2)
            text3 = root.widgets[5].get()
            print("変更後のブランチ : " + text3)
            text4 = root.widgets[7].get()
            print("クライアントID : " + text4)
            text5 = root.widgets[9].get()
            print("シークレット : " + text5)
            root.destroy()

        # ルート参照から到達できるように生成したwidgetを保持
        widget_dict = OrderedDict()
        for i, component in enumerate(load_widget()):
            widget = None
            if component['type'] == 'Label':
                widget = Tk.Label(root, text=component['text'])
            elif component['type'] == 'Entry':
                widget = Tk.Entry(root, width=component['width'])
                if 'focus_set' in component:
                    if component['focus_set']:
                        widget.focus_set()
            elif component['type'] == 'Button':
                widget = Tk.Button(root, text=component['text'] , command=lambda: func(root))
            else:
                assert widget is not None, component['type']
            widget.place(relx=component['relx'], rely=component['rely'])
            widget_dict[i] = widget

        return widget_dict

    root = Tk.Tk()
    root.geometry("1000x600")
    root.widgets = create_widgets(root)

    # 作成したwidgetを出力
    root.mainloop()
    
    return text1, text2, text3, text4, text5