#ワードリスト入れればchangeが0になるまで名詞リストの接続を行っていく
def connect(w_l, num=1, c=0,cnt=0):
    """
    input : {word_list:[['word','por'],['word','por'],['word','por'],...]
            num : default 1 [number of cahnge]
            c : default 1 [connect count]
            }
    output : {conected_word_list: [[word,por],[word,por]...]}
    """
    if num==0 or len(w_l)==0 or len(w_l)==1:
        #print("fin:{}".format(c))
        return w_l
    al_word_list=w_l
    change=0
    #cnt=0
    new_list=[]
    for ind,mat in enumerate(al_word_list):
    #     if cnt==1:
    #         cnt=0
        if ind==len(al_word_list)-1:
            if cnt==1:
                cnt=0
            else:
                #cnt=0
                new_list.append(mat)
        elif al_word_list[ind][1]==al_word_list[ind+1][1] and cnt==0 and al_word_list[ind+1][1]!="記号":#記号は連結させない。
            new_list.append([al_word_list[ind][0]+al_word_list[ind+1][0],al_word_list[ind][1]])
            change+=1
            cnt=1
        elif al_word_list[ind][1]=='接頭詞' and cnt==0 and al_word_list[ind+1][1]!="記号":#接頭詞は次の名詞と連結させる。
            new_list.append([al_word_list[ind][0]+al_word_list[ind+1][0],al_word_list[ind+1][1]])
            change+=1
            cnt=1
        elif al_word_list[ind][1]=='名詞' and cnt==0 and al_word_list[ind+1][0] in ["・","-"] and al_word_list[ind+1][1]=="記号":
            #-,・は次の名詞と連結させる。ただし語彙として少なくなるのでword2vecには出てこなくなる可能性が高い
            new_list.append([al_word_list[ind][0]+al_word_list[ind+1][0],al_word_list[ind][1]])
            change+=1
            cnt=1
        else:
            if cnt==1:
                cnt=0
            else:
                new_list.append(mat)
    c+=1
    #print(new_list)
    return connect(new_list,num=change,c=c,cnt=cnt)

def create_word_list(al_text,tagger,prog=False):
    from tqdm import tqdm
    """
    input : {text:
                [
                ["sentence"],
                ["sentence"],
                ["sentence"], ...
                ]
             tagger:MeCab tagger

    output : {word_list:[[word,por],
                         [word,por],
                         [word,por],...]
    """
    #listを投げる
    word_list=[]

    if prog:
        text_list=tqdm(al_text)
    else:
        text_list=al_text

    for t in text_list:
        if len(t)==0:#空白なら消す（。と\ｎの間の空白消し）
            pass
        else:
            cl=tagger.parse(t)
            word_list+=[[s.split('\t')[0],s.split('\t')[1].split(",")[0]] for s in cl.splitlines()[:-1]]

    return word_list
"""
if __name__ == '__main__':
    in_path=input('input path:')
    out_path=input('output path:')
    '''
    今は改行で随時とってきてるけども
    オンメモリにできるなら、読み込んでsplitlines処理したものをtqdmで回せば安心感出る。
    enumerateはbereak検査用
    ファイル保存はa(append)制にしてるので加わっていてしまうことに注意
    '''
    for i, sent in tqdm(enumerate(open(in_path,'rb'))):
        # if i==2:
        #     break
        # else:
        p1 = re.compile(r'。|\n|\s')
        p0 = re.compile(r'\r|\t|\u3000|\n')
        tagger = MeCab.Tagger('mecab -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        try:
            data = sent.decode('sjis')
        except:
            try:
                data=sent.decode('utf-8')
            except:
                data=sent.decode('cp932')
        al_data=p0.sub('',data)
        #al_text=al_text.split('。')#
        al_data = p1.split(al_data)
        al_data = [s + '。' for s in al_data if s != '']
        li = create_word_list(al_data, tagger)
        res = connect(li,1,1)
        tmp = create_tmp(res)
        #por = create_por(res)
        with open(out_path,'a') as f:
            f.write(tmp)
    print("Finished.")
"""
