#!/usr/bin/env python
# coding: utf-8

# In[1]:


# モジュールインポート
import requests
import json
import base64
from tqdm import tqdm_notebook as tqdm
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import glob


def file_select(file_path, file_type, message):

    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()

    # ファイルのタイプを選択
    fTyp = [("", "*." + file_type)]

    iDir = os.path.abspath(os.path.dirname(file_path))
    tkinter.messagebox.showinfo('ファイルの選択',message+'を選択してください')
    file_name = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

    # 処理ファイル名の出力
    tkinter.messagebox.showinfo('選択されたファイル',file_name)
    
    root.destroy()
    
    return file_name


from tkinter import filedialog

def folder_select(directory = 'C:\\'):
    
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo('ローカルリポジトリの選択','ローカルリポジトリのディレクトリを選択してください')
    fld = filedialog.askdirectory(initialdir = directory) 
    root.destroy()
    
    return fld

def get_text(message):
    
    root2 = tkinter.Tk()

    # ウインドウのタイトルを定義する
    root2.title(message + 'の入力')

    # ここでウインドウサイズを定義する
    root2.geometry('400x300')


    # ボタンが押されたら呼び出される関数
    def get_file_name(text):
        global written_text
        written_text = text
        tkinter.messagebox.showinfo('info', text)
        root2.destroy()

    # ラベルを使って文字を画面上に出す
    Static1 = tkinter.Label(text=message+'を入力')
    Static1.pack()

    # Entryを出現させる
    Entry1 = tkinter.Entry(width=50)                   # widthプロパティで大きさを変える
    Entry1.insert(tkinter.END, message+'を入力してください')        # 最初から文字を入れておく
    Entry1.pack()


    # Buttonを設置してみる
    Button1 = tkinter.Button(text=u'決定', width=20, command=lambda: get_file_name(Entry1.get()))# 関数に引数を渡す場合は、commandオプションとlambda式を使う
    Button1.pack()

    root2.mainloop()
    
    root2.destroy
    return written_text

