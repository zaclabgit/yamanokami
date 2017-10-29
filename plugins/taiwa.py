from slackbot.bot import default_reply
import MeCab
import random
import gensim
import numpy as np
import pickle
import heapq
import os

base = os.path.dirname(os.path.abspath(__file__))

# モデルの読み込み
from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format(base + '/models/entity_vector.model.bin', binary=True)

# mecabの準備
tagger = MeCab.Tagger("-Ochasen")

# 辞書の準備 dict[que,(vec,reps),...]
import os.path
vocab_path = base + '/dictionary/w2v_vocab.pickle'
if os.path.exists(vocab_path):
    with open(vocab_path, mode='rb') as f:
        vocab = pickle.load(f)
else : #辞書がないときのとりあえずの語彙
    vocab = {'山':(model['山'],'山')}

print("準備完了")

def seq2vec(seq):
    count = 0
    vec = np.zeros(200)
    for word in tagger.parse(seq).split('\n'):
        w = word.split('\t')[0]
        if w in model :
            count += 1
            vec += model[w]
    return vec / count

# dict[que,(vec,reps),...]を辞書に追加
# queが同じ場合は'|'で区切ってrepsに追加(現状repsとqueが一緒なのでこの処理は必要なし)
# pickleで保存
def learn(seq):
    if not seq in vocab: # 新しい語彙の場合
        vocab[seq] = (seq2vec(seq),seq)
    with open(vocab_path, mode='wb') as f:
        pickle.dump(vocab, f)
    print("学習しました:",seq)

# cos類似度
def cos_sim(v1,v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# dict[que:(vec,rep),...]から最も近い文章のランキング上位3つから
def vocab_choicer(user_vec):
    rank_que = []
    for que,(vec,rep)  in vocab.items():
        nowsim = cos_sim(user_vec,vec)
        rank_que.append((nowsim, rep))
    if len(rank_que) >= 10 :
        top3 =  heapq.nlargest(10,rank_que)
        print("お返事")
        print(top3)
        return top3[random.randint(0,2)][1]
    else :
        return rank_que[random.randint(0,len(rank_que)-1)][1]

@default_reply()
def response_by_dictionary(message):
    text = message.body['text'] # メッセージを取り出す
    response = vocab_choicer(seq2vec(text))
    learn(text)
    message.reply(response)
