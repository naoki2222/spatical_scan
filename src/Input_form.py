import tkinter as tk
import tkinter.messagebox as tmb
from collections import OrderedDict

def data_get():

    def load_widget():
        widget_list = list()
        widget_list.append({'type': 'Label', 'text': "リポジトリのURL :", 'relx': 0.01, 'rely': 0.005})
        widget_list.append({'type': 'Entry', 'width': 80, 'relx': 0.11, 'rely': 0.005, 'focus_set': True})
        widget_list.append({'type': 'Label', 'text': "変更前のブランチ :", 'relx': 0.01, 'rely': 0.055})
        widget_list.append({'type': 'Entry', 'width': 20, 'relx': 0.11, 'rely': 0.055})
        widget_list.append({'type': 'Label', 'text': "変更後のブランチ :", 'relx': 0.01, 'rely': 0.105})
        widget_list.append({'type': 'Entry', 'width': 20, 'relx': 0.11, 'rely': 0.105})
        widget_list.append({'type': 'Label', 'text': "クライアントID :", 'relx': 0.01, 'rely': 0.155})
        widget_list.append({'type': 'Entry', 'width': 40, 'relx': 0.11, 'rely': 0.155})
        widget_list.append({'type': 'Label', 'text': "シークレット :", 'relx': 0.01, 'rely': 0.205})
        widget_list.append({'type': 'Entry', 'width': 40, 'relx': 0.11, 'rely': 0.205})
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
                widget = tk.Label(root, text=component['text'])
            elif component['type'] == 'Entry':
                widget = tk.Entry(root, width=component['width'])
                if 'focus_set' in component:
                    if component['focus_set']:
                        widget.focus_set()
            elif component['type'] == 'Button':
                widget = tk.Button(root, text=component['text'] , command=lambda: func(root))
            else:
                assert widget is not None, component['type']
            widget.place(relx=component['relx'], rely=component['rely'])
            widget_dict[i] = widget

        return widget_dict

    root = tk.Tk()
    root.geometry("1000x600")
    root.widgets = create_widgets(root)

    root.title("取得データの入力")
    root.mainloop()
    
    return text1, text2, text3, text4, text5




def data_get2():

    root = tk.Tk()

    def func():
        global text6
        global text7
        global text8
        global text9
        global text10
        global text11

        text6 = sv1.get()
        print("CSの関数: " + text6)
        text7 = sv2.get()
        print("停止条件の種類 : " + text7)
        text8 = sv3.get()
        print("グラフの種類 : " + text8)
        text9 = tS1.get()
        print("しきい値 : " + text9)
        text10 = tS2.get()
        print("CSの実行回数 : " + text10)
        text11 = tS3.get()
        print("CSのホップ数 : " + text11)
        root.destroy()


    # OptionMenu 1
    tk.Label(root, text="CSのタイプ選択").grid(row=1, sticky="e")
    sv1 = tk.StringVar()
    sv1.set('single')
    tO = tk.OptionMenu(root, sv1, 'single', 'repeat')
    tO.grid(row=1, column=1, padx=10, pady=10)
    
    # OptionMenu 2
    tk.Label(root, text="停止条件の種類").grid(row=2, sticky="e")
    sv2 = tk.StringVar()
    sv2.set('default')
    tO2 = tk.OptionMenu(root, sv2, 'default', 'hop')
    tO2.grid(row=2, column=1, padx=10, pady=10)
    
    # OptionMenu 3
    tk.Label(root, text="グラフの種類").grid(row=3, sticky="e")
    sv3 = tk.StringVar()
    sv3.set('有効グラフ')
    tO3 = tk.OptionMenu(root, sv3, '有効グラフ', '無向グラフ')
    tO3.grid(row=3, column=1, padx=10, pady=10)

    # Spinbox 1
    tk.Label(root, text="しきい値").grid(row=1, column=2, sticky="e")
    tS1 = tk.Spinbox(root, values=(0.1,  0.2, 0.25, 0.5))
    tS1.grid(row=1, column=3, padx=10, pady=10)
    
    # Spinbox 2
    tk.Label(root, text="CSの実行回数").grid(row=2, column=2, sticky="e")
    tS2 = tk.Spinbox(root, values=(1,2,3,4,5,6,7,8,9,10))
    tS2.grid(row=2, column=3, padx=10, pady=10)

    # Spinbox 9
    tk.Label(root, text="CSのhop数").grid(row=3, column=2, sticky="e")
    tS3 = tk.Spinbox(root, values=(1,2,3,4,5,6,7,8,9,10))
    tS3.grid(row=3, column=3, padx=10, pady=10)

    # button 1
    tk.Button(root, text='保存' , command=lambda: func()).grid(row=3, column=4, padx=10, pady=10)


    root.title("実験条件の入力")
    root.mainloop()
    
    return  text6, text7, text8, text9, text10, text11