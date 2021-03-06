# モジュールインポート
import requests
import json
import base64
from tqdm import tqdm_notebook as tqdm
import glob
import os

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

###########################################################################################################################################
from AST.ast_processor import AstProcessor
from AST.basic_info_listener import BasicInfoListener

def get_dependencies(repo_path):

    import_dependencies = []
    exception_dependencies = []
    class_interface_dic = {}
    extends_list = []
    interface_extends_list = []
    implements_list = []
    
    #ローカルリポジトリのファイル名を取得
    file_list = glob.glob(repo_path + '/**/*.java',recursive=True)

    #ファイルの依存関係の取得
    print('get dependencies')
    for i in tqdm(range(len(file_list))):
        file_list[i] = file_list[i].replace('\\', '/')
        target_file_path = file_list[i]
        ast_info = AstProcessor(BasicInfoListener()).execute(target_file_path)

        #importしているファイル名の取得
        if ast_info['imports'] != []:
            for j in range(len(ast_info['imports'])):
                end = ast_info['imports'][j].replace('.','/')+'.java'
                if [target_file_path.replace(repo_path+'/',''), end] not in import_dependencies:
                    import_dependencies.append([target_file_path.replace(repo_path+'/',''), end])
                
        #例外処理として呼ばれているファイル名の取得
        if ast_info['exception'] != []:
            for j in range(len(ast_info['exception'])):
                end = '/' + ast_info['exception'][j]+'.java'
                if [target_file_path.replace(repo_path+'/',''), end] not in exception_dependencies:
                    exception_dependencies.append([target_file_path.replace(repo_path+'/',''), end])

        class_interface_dic[target_file_path.split('/')[-1].split('.')[0]] = target_file_path

        if ast_info['extends'] != '':
            extends_list.append([file_list[i], ast_info['extends']])
        if ast_info['interface_extends'] != []:
            interface_extends_list = interface_extends_list + ast_info['interface_extends']
        if ast_info['implements'] != []:
            for impl in range(len(ast_info['implements'])):
                implements_list.append([file_list[i], ast_info['implements'][impl]])

    
    #interface_extendsクラス名をファイル名に変更する
    for i in interface_extends_list:
        if i[0] in class_interface_dic.keys():
            i[0] = class_interface_dic[i[0]]
        if i[1] in class_interface_dic.keys():
            i[1] = class_interface_dic[i[1]]      
    
    #クラス名をファイル名
    for e in range(len(extends_list)):
        if extends_list[e][1] in class_interface_dic.keys():
            extends_list[e][1] = class_interface_dic[extends_list[e][1]]
           
    for imp in range(len(implements_list)):
        if implements_list[imp][1] in class_interface_dic.keys():
            implements_list[imp][1] = class_interface_dic[implements_list[imp][1]]

    return import_dependencies, exception_dependencies, class_interface_dic, extends_list, interface_extends_list, implements_list

#########################################################################################################################################

def get_file_lines(repo_path):

    line_list = []
    
    for p in glob.glob(repo_path + '/**/*.java', recursive=True):
        if os.path.isfile(p):
            line = len(open(p, encoding="utf-8").readlines())
            p = p.replace('\\', '/')
            p = p.replace(repo_path+'/', '')
            line_list.append([p,line])

    return line_list
#ブランチ, タグ間での変更を見る

########################################################################################################################################
'''
ファイル行数の取得
'''
############################################################################################################
def get_java_line(repo_path, repo_url, from_ver, to_ver, client_id, client_secret):
    
    #行数データの取得
    java_line = get_file_lines(repo_path)

    #コミットの取得
    _,list_commit = commit_reseach(repo_url, from_ver, to_ver, client_id, client_secret)

    #javaファイルのみのコミットに限定する
    commit_set = [] 
    java_set = []   #コミットごとにファイルをまとめる
    for i in range(len(list_commit)):
        for j in range(len(list_commit[i])):
            if ('.java' in list_commit[i][j][0]):
                java_set.append(list_commit[i][j])

        if java_set == []:
            continue
        else:
            commit_set.append(java_set)
            java_set = []

    #それぞれの定義にしたがって行数を計算する
    java_line = sum_line_generator1(java_line, commit_set)
    #java_line = sum_line_generator2(java_line, commit_set)

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

