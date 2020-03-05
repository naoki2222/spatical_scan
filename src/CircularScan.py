#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import numpy.random as rd
import scipy.stats as st
import matplotlib.pyplot as plt
from numpy.random import *
import pandas as pd
from tqdm import tqdm_notebook as tqdm
import openpyxl

#空間スキャン検定

######################################################## 関数定義 ##########################################################################

#lineは行数のリスト、commitはコミットのリスト
def G_data(line,commit):
    n_G = 0
    c_G = 0
    for i in range(len(line)):
        n_G = line[i][1] + n_G
    for j in range(len(commit)):  
        c_G = commit[j][1] + c_G

    return n_G,c_G

#####################################################################################################################

############################################################################################################################################

#list_Zは領域の名前がリストになったもの,line_Gは[name,行数],commit_Gは[name,変更行数]のリスト
def Z_data(list_Z,line_G,commit_G):
    
    n_Z = 0
    c_Z = 0
    
    for i in range(len(list_Z)):
        for j in range(len(line_G)):
            if list_Z[i] == line_G[j][0]:
                n_Z = line_G[j][1] + n_Z
                
                
    for i in range(len(list_Z)):
        for j in range(len(commit_G)):
            if list_Z[i] == commit_G[j][0]:
                c_Z = commit_G[j][1] + c_Z
                
    return n_Z,c_Z
#########################################################################################################

#########################################################################################################

#2項分布でのLLRモデル

import math
def LLR(n_G,c_G,n_Z,c_Z):#n:行数 c:属性値   _G:全体集合の   _Z:部分集合の     

    LLR = 0
    
    if ((c_G == c_Z) or (n_G == n_Z) or ((c_Z/n_Z) <= (c_G - c_Z)/(n_G - n_Z))):
        return 0
        
    else:
        LLR = c_Z * math.log(c_Z/n_Z) +  (n_Z - c_Z)*math.log(1-c_Z/n_Z)  +  (c_G-c_Z)*math.log((c_G-c_Z)/(n_G-n_Z)) + ((n_G-n_Z)-(c_G-c_Z))*math.log(1-(c_G-c_Z)/(n_G-n_Z)) - c_G*math.log(c_G/n_G) - (n_G-c_G)*math.log(1-c_G/n_G)            
        return LLR
    


##############################################################################################################################################
#file_name: java_lineの１つの要素['str',int]
#relation_list : モジュールの依存関係のリスト [[str,str],[str,str],・・・]
#threshold : スキャン終了の条件（しきい値） int
#javaline : ファイルのコード行数のリスト [[str,int],[str,int]・・・]
#javacommit : ファイルの修正行数のリスト [[str,int],[str,int]・・・]

#出力 : file_data[0]中心で実施されたCSによって得られた領域群Zの候補リスト : [[str],[str,str,str,・・・],・・・]

def C_scan(file_data,java_module,threshold,java_line,java_commit):  
    
    group_Z = [file_data[0]]
    group_Zs = [group_Z]
    n_G,c_G = G_data(java_line, java_commit)
    
    while True:
        adj_list = []
        for i in group_Z:
            for j in java_module:
                if (i == j[1]) and (j[0] not in group_Z) and (j[0] not in adj_list):
                    adj_list = adj_list + [j[0]]

        if adj_list == []:
            break

        adj_list = adj_list + group_Z
        n_Z,c_Z = Z_data(adj_list,java_line,java_commit)

        if (threshold >= n_Z/n_G):
            group_Z = adj_list
            group_Zs.append(group_Z)
        else:
            break
    
    return group_Zs
##############################################################################################################################################

#file_name: java_lineの１つの要素['str',int]
#relation_list : モジュールの依存関係のリスト [[str,str],[str,str],・・・]
#threshold : スキャン終了の条件（しきい値） int
#javaline : ファイルのコード行数のリスト [[str,int],[str,int]・・・]
#javacommit : ファイルの修正行数のリスト [[str,int],[str,int]・・・]

#出力 : file_data[0]中心で実施されたCSによって得られた領域群Zの候補リスト : [[str],[str,str,str,・・・],・・・]

def C_scan_hops(file_data,java_module,threshold,java_line,java_commit,hop_count):  
    
    group_Z = [file_data[0]]
    group_Zs = [group_Z]
    n_G,c_G = G_data(java_line, java_commit)
    
    for count in range(hop_count):
        #adj_list : ノードと近傍のノードリスト
        adj_list = []
        for i in group_Z:
            for j in java_module:
                if (i == j[1]) and (j[0] not in group_Z) and (j[0] not in adj_list):
                    adj_list = adj_list + [j[0]]

        adj_list = group_Z + adj_list

        if adj_list != group_Z:
            group_Z = adj_list
            group_Zs.append(group_Z)
        else:
            break
    
    return group_Zs
##############################################################################################################################################

#####################################################################################################################
#2項分布でのLLR分布作成（モンテカルロ）

#value : ポアソンの期待値
#count 乱数発生回数
#p : 帰無仮説下での属性確率
#n_G : 全体の母集団(全体の総行数)
#Z   : 調べるファイルの集合（リスト）
#n_Z : Zの母集団(Zの行数)

def LLR_distribution(count,p,n_G,Z,java_line):
    
    distribution = []
    
    for i in range(count):
        
        c_Z_list = []
        n_Z = 0
        c_Z = 0
    
        for i in range(len(java_line)):
            c_Z_list.append(binomial(n=java_line[i][1], p=p))
        
        c_G = sum(c_Z_list)
        
        for i in range(len(java_line)):
            if(java_line[i][0] in Z):
                c_Z = c_Z_list[i] + c_Z
                n_Z = java_line[i][1] + n_Z

        distribution.append(LLR(n_G,c_G,n_Z,c_Z))
        
        distribution.sort()
    
    return distribution


#############################################################################################################################################

#####################################################################################################################
#入力
#LLR_dis : LLR分布のリスト
#LLR_value : 実際のデータでのLLRの計算結果
#Level : 有意水準

#出力
#result : 検定結果(trueは有意)
#p_value : p値

def Monte_Carlo(LLR_dis, LLR_value,Level):
    
    deno = len(LLR_dis)
    mole = 0
    
    for i in range(len(LLR_dis)):
        if (LLR_dis[i] > LLR_value):
            mole = mole+1
    
    p_value = (mole+1) / (deno+1)
    
    return p_value

##########################################################################################################################################

##########################################################################################################################################
#scan_typeでのCSのタイプを選択
#'hop'ならC_scan_hops()を使用.
#'default' #それ以外ならC_scan()を使用する

#C_scan_hops()の設定
#iter_num : CSの反復回数
#hop_count  : C_scan_hops()を使うときのホップ数

#C_scanの設定
#threshold = 0.25   #領域拡大の停止条件(threshold=0.05 → 領域の行数が全体の5%以上になったら停止)

def CS_run(java_line, java_commit, java_module, prob_list, scan_type, iter_num, hop_count, threshold):

    #repeat_CS_listは各反復でLLRが1位になった領域と領域のp値を保存するリスト
    repeat_CS_list = []
    repeat_CS_detail_list = []

    for repeat_count in tqdm(range(iter_num)):
        #前回の結果でもっともLLRが高かったファイルの集合→cut_list
        #cut_list => ここにあるファイルを実験から除外
        print('--------------------------repeat_count------------------------- : ' + str(repeat_count))


        if repeat_count != 0:
            cut_list = []
            for i in LLR_value_list[0][0]:
                cut_list = cut_list + [i]

            java_module_2 = []
            java_commit_2 = []
            java_line_2 = []
            prob_list_2 = []

            print('cut_list')
            print(cut_list)

            print('create file2')
            for i in  tqdm(java_module):
                if i[0] not in cut_list and i[1] not in cut_list:
                    java_module_2.append(i)

            for i in  tqdm(java_line):
                if i[0] not in cut_list:
                    java_line_2.append(i)

            for i in  tqdm(java_commit):
                if i[0] not in cut_list:
                    java_commit_2.append(i)

            for i in  tqdm(prob_list):
                if i[0] not in cut_list:
                    prob_list_2.append(i)



            print('各ファイルのチェック')        
            print('java_module : ' + str(len(java_module)))
            print('java_commit : ' + str(len(java_commit)))
            print('java_line : ' + str(len(java_line)))
            print('prob_list : ' + str(len(prob_list)))

            print('java_module_2 : ' + str(len(java_module_2)))
            print('java_commit_2 : ' + str(len(java_commit_2)))
            print('java_line_2 : ' + str(len(java_line_2)))
            print('prob_list_2 : ' + str(len(prob_list_2)))


            #各データの更新
            java_module = java_module_2
            java_commit = java_commit_2
            java_line = java_line_2
            prob_list = prob_list_2


        #モジュール依存関係の内,実験に関係のあるものだけを見つける.
        # (グラフの両辺がprob_moduleにあるファイルの名前になっている.) 

        print('prob, prob_moduleの構築')
        prob1 = []
        for i in prob_list:
            prob1.append(i[0])

        prob1[0]

        prob_module = []
        for i in java_module:
            if (i[0] in prob1) and (i[1] in prob1):
                prob_module.append(i)


        #Circular_scanの実施
        print('CSの実行')
        Z_list = []    #CSによってできた領域群Zのリスト
        LLR_value_list = []  

        #CSの
        if scan_type == 'hop':
            for i in tqdm(java_line):
                Z_list = Z_list + C_scan_hops(i,prob_module,threshold,java_line,java_commit,hop_count)
        else:
            for i in tqdm(java_line):
                Z_list = Z_list + C_scan(i,prob_module,threshold,java_line,java_commit)

        print('finish')
        print('Number of Z  : ' + str(len(Z_list)))

        #LLRの計算
        print('calculate LLR')
        for i in tqdm(Z_list):
            n_Z,c_Z = Z_data(i,java_line,java_commit)
            n_G,c_G = G_data(java_line, java_commit)
            LLR_value_list.append([i,LLR(n_G,c_G,n_Z,c_Z),n_Z,c_Z])
            LLR_value_list = sorted(LLR_value_list, key=lambda x:x[1], reverse=True)

        #検定の実施とその結果のまとめ

        #LLR_value_list[z][領域群Zの中身, LLRの値, n_Z, c_Z]
        #input_LLR[領域群Zの中身, LLRの値, n_Z, c_Z]

        #LLRが最大となった領域群を指定
        input_LLR = LLR_value_list[0]

        n_G,c_G = G_data(java_line,java_commit)
        n_Z,c_Z = Z_data(input_LLR[0],java_line,java_commit)
        p = c_G / n_G

        print('calculate p value')
        dis =  LLR_distribution(9999,p,n_G,input_LLR[0],java_line)
        p_value = Monte_Carlo(dis,input_LLR[1], 0.01)
        print('pval_finish')

        print('create repeat_CS_list')
        repeat_CS_list.append([LLR_value_list[0][0] ,p_value])
        repeat_CS_detail_list.append([LLR_value_list[0][0], len(LLR_value_list[0][0]),c_Z/n_Z, c_Z, n_Z])

        print('repeat_CS_list のデータ数')
        print(len(repeat_CS_list))
        
    return repeat_CS_list

