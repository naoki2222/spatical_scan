#!/usr/bin/env python
# coding: utf-8

# In[2]:


# モジュールインポート
import requests
import json
import base64
from tqdm import tqdm_notebook as tqdm
import glob

#名前が複数出てきているコミットを一つにまとめる.
def search_add(list1,list2):
    if(list1 == []):
        list1.append(list2)
        return list1
    else:
        for i in range(len(list1)):
            if(list1[i][0] == list2[0]):
                list1[i][1] = (list1[i][1] + list2[1])
                return list1

        list1.append(list2)
        return list1
    
    
#ファイルの行数の総和((S1 + S2) + (S2 + S3) + ・・・ + (Sn-1 + Sn))を作る.
# java_line : ['ファイル名', 'ファイルの行数']
# java_commit : [['ファイル名', 'ファイルの修正行数(add+del)', 'ファイル追加と削除の差(add-del)'],[  ]・・・]

def sum_line_generator1(java_line, java_commit):

    #初期化
    sum_line_list = []
    S = [0] * (len(java_commit)+1)
    sum_line = 0
    
    #計算
    for i in range(len(java_line)):
        S[0] = java_line[i][1]
        sum_line = 0
        for j in range(len(java_commit)):
            for z in range(len(java_commit[j])):
                if java_line[i][0] == java_commit[j][z][0]:
                    S[j+1] = S[j] - java_commit[j][z][2]
                else:
                    S[j+1] = S[j]
            sum_line = sum_line + S[j+1] + S[j]
        sum_line_list.append([java_line[i][0],sum_line])

    return sum_line_list


#行の最大値 × コミット回数

def sum_line_generator2(java_line,java_commit):
    
    #初期化
    sum_line_list = []
    S = [0] * (len(java_commit)+1)
    
    #計算
    for i in range(len(java_line)):
        S[0] = java_line[0]
        for j in range(len(java_commit)):
            if j == 0:
                S[j] = java_line[i][1]
            else:
                for z in range(len(java_commit[j])):
                    if java_line[i][0] == java_commit[j][z][0]:
                        S[j+1] = S[j] - java_commit[j][z][2]
                    else:
                        S[j+1] = S[j]

        S_max = max(S) * len(java_commit)
        sum_line_list.append([java_line[i][0],S_max])

    return sum_line_list


#コミット情報の取得
#入力 (リポジトリのurl, コミット情報の観測のスタートとなるbranch,コミット情報の観測の終了地点となるbranch, クライアントのid, クライアントシークレット)
#出力 commit_list : [[ファイルの名前],[修正行数]]
     #commit_list2 : [[[ファイルの名前, ファイルの修正行数],[ファイルの名前, ファイルの修正行数]],  ・・・] ※コミット毎に修正がまとめられている

def commit_reseach(repository_url, from_ver, to_ver, client_id, client_secret):

    commit_list = []
    commits_set = []
    commit_list2 = []
    
    repository_url = repository_url.replace('.git', '/compare/{f}...{t}')
    api = repository_url.replace('https://github.com/', 'https://api.github.com/repos/')
    print('api : ' +  api)
    url = api.format(f=from_ver, t=to_ver)
    
    r = requests.get(url,auth=(client_id, client_secret))
    data = json.loads(r.text)
    
    for i in tqdm(range(len(data['commits']))):
        
        url = data['commits'][i]['url']
        r = requests.get(url,auth=(client_id, client_secret))
        data2 = json.loads(r.text)
        
        for j in range(len(data2['files'])):
            
            filename = data2['files'][j]['filename']
            additions = data2['files'][j]['additions']
            deletions = data2['files'][j]['deletions']
            changes = data2['files'][j]['changes']
            commits_set.append([filename,changes,additions-deletions])
            commit_list.append([filename,changes])
        commit_list2.append(commits_set)
        commits_set = []

    return commit_list, commit_list2

def get_file_lines(pathname, recursive=True):

    line_list = []
    
    for p in glob.glob(pathname + '/**/*.java', recursive=recursive):
        if os.path.isfile(p):
            line = len(open(p).readlines())
            p = p.replace('\\', '/')
            p = p.replace(pathname+'/', '')
            line_list.append([p,line])

    return line_list

#ブランチ, タグ間での変更を見る

###########################################################################################################
'''
ファイル行数の取得
'''
############################################################################################################
def get_java_line(local_ripository_path, repo_url, from_ver, to_ver, client_id, client_secret):
    
    #テキストデータ読み込み
    java_line = get_file_lines(local_ripository_path, recursive=True)

    #コミットの取得
    _,list_commit = commit_reseach(repo_url, from_ver, to_ver, client_id, client_secret)


    #moduleディレクトリのファイルのみのコミットリスト
    java_commit = []
    java_set = []  #コミットごとにファイルをまとめる
    for i in range(len(list_commit)):
        for j in range(len(list_commit[i])):
            if ('.java' in list_commit[i][j][0]):
                java_set.append(list_commit[i][j])

        if java_set == []:
            continue
        else:
            java_commit.append(java_set)
            java_set = []


    #java_commitのファイル名をjava_lineの名前に合わせる.
    for i in java_commit:
        for j in java_line:
            if j[0] in i[0]:
                i[0] = j[0]

    java_commit.reverse()

    java_line = sum_line_generator1(java_line, java_commit)
    #java_line = sum_line_generator2(java_line, java_commit)


    #java_line
    #[0]  :  ファイルの名前
    #[1]  :  Siの値
    
    return java_line


###########################################################################################################

'''
コミットの調査
'''

###########################################################################################################   
def get_java_commit(repo_url, from_ver, to_ver, client_id, client_secret, java_line):
    
    #コミット情報の取得
    list1,_ = commit_reseach(repo_url, from_ver, to_ver, client_id, client_secret)

    #2回以上同じファイルでコミットがあった場合,コミット行数を足してまとめる。
    list_commit = []
    for i in range(len(list1)):
        list_commit = search_add(list_commit,list1[i])


    #javaファイルのみのコミットリストを作成(java_commit)
    java_commit = []
    for i in range(len(list_commit)):

        #if ('src/' in list_commit[i][0]) and ('.java' in list_commit[i][0]):
        if ('.java' in list_commit[i][0]):
            java_commit.append(list_commit[i])


    #重複回避
    delete_list = []
    for i in range(len(java_commit)):
        for j in range(len(java_commit)):
            if(java_commit[i][0] == java_commit[j][0]) and i != j and i > j:
                delete_list.append(java_commit[i])
                delete_list.append(java_commit[j])
                java_commit.append([java_commit[i][0],(java_commit[i][1]+java_commit[j][1])])

    java_commit = sorted(java_commit, key=lambda x:x[1], reverse=True)


    # java_commit内のファイルの名前をjava_lineのファイル名の形式に合わせる

    for i in java_commit:
        for j in java_line:
            if j[0] in i[0]:
                i[0] = j[0]

    return java_commit
#############################################################################################################
    
    
############################################################################################################
'''
モジュール依存関係の読み込み
'''
###########################################################################################################
def get_java_module(java_line, dot_name, interaction_type):

    col0 = [] #始点の頂点集合
    col1 = [] #終点の頂点集合
    java_module = []
    interaction_type = interaction_type
    
    for i, line in enumerate(open(dot_name)): # ファイルを開いて一行一行読み込む

        c = line.split("->")

        c[0]=c[0].strip()
        c[0]=c[0].strip('  ')
        c[0]=c[0].strip('"')

        c[1]=c[1].strip()
        c[1]=c[1].strip('  ')
        c[1]=c[1].strip(";")
        c[1]=c[1].strip('"')

        c[0] =  c[0].replace('.', '/')
        c[0] =  c[0] + '.java'
        col0.append((c[0])) 
        c[1] =  c[1].replace('.', '/')
        c[1] =  c[1] + '.java'
        col1.append((c[1])) 

    #辺のリストを作成
    edge = []
    for x, y in tqdm(zip(col0, col1)):
        if ([x,y] not in edge):
            edge.append([x,y])

    java_module = edge
            
    ###########################################################################################################
    
    #txtファイル→グラフへの変換

    col0 = [] #始点の頂点集合
    col1 = [] #終点の頂点集合

    if interaction_type == 'undirect':
    
        for i, line in enumerate(open(dot_name)): # ファイルを開いて一行一行読み込む

            c = line.split("->")

            c[0]=c[0].strip()
            c[0]=c[0].strip('  ')
            c[0]=c[0].strip('"')

            c[1]=c[1].strip()
            c[1]=c[1].strip('  ')
            c[1]=c[1].strip(";")
            c[1]=c[1].strip('"')

            c[0] =  c[0].replace('.', '/')
            c[0] =  c[0] + '.java'
            col0.append((c[0])) 
            c[1] =  c[1].replace('.', '/')
            c[1] =  c[1] + '.java'
            col1.append((c[1]))

        #辺のリストを作成
        #edge2はedgeの中身を逆転させたもの
        edge2 = []

        for x, y in tqdm(zip(col0, col1)):
            if ([y,x] not in edge2):
                edge2.append([y,x])

        #java_moduleはモジュール依存関係のグラフ
        java_module = edge + edge2


    #java_lineのファイル名にjava_moduleのファイル名をそろえる.
    for i in tqdm(java_module):
        for j in java_line:
            if i[0] in j[0]:
                i[0] = j[0]
            if i[1] in j[0]:
                i[1] = j[0]
    
    return java_module


#############################################################################################################
#ファイルごとの属性確率を求める
#java_lineの長さ == prob_listの長さ
#prob_list    :     属性確率のリスト

def get_prob_list(java_line, java_commit):

    prob_list = []
    prob_name_list = []

    for i in range(len(java_line)):
        for j in range(len(java_commit)):
            if(java_line[i][0] == java_commit[j][0]):
                prob = (java_commit[j][1] / java_line[i][1])
                prob_list.append([java_line[i][0],prob])
                prob_name_list.append(java_line[i][0])

    for i in range(len(java_line)):
        if(java_line[i][0] not in prob_name_list):
            prob_list.append([java_line[i][0],0])


    prob_list = sorted(prob_list, key=lambda x:x[1], reverse=True)
    
    return prob_list

