import codecs
from janome.tokenizer import Tokenizer
from collections import Counter

class JanomeUtil():
    def __init__(self):
        self.t = Tokenizer()

    def get_tokens(self, txt):
        return [token for token in self.t.tokenize(txt) if token.reading is not '*']


def load_pn_dict():
    with codecs.open('./pn_ja.dic', 'r', 'shift_jis') as f:
        lines = f.readlines()
    return {'{}'.format(line.split(':')[0]): float(line.split(':')[3]) for line in lines}


def get_pn_scores(tokens, pn_dic):
    scores = []

    for surface in [t.surface for t in tokens if t.part_of_speech.split(',')[0] in ['動詞', '名詞', '形容詞', '副詞']]:
        try:
            if -0.8 > float(pn_dic[surface]) or float(pn_dic[surface]) > 0.1:
                scores.append(pn_dic[surface])
        except:
            continue
    return scores


def load_wago_dict():
    with codecs.open('./wago.121808.pn', 'r') as f:
        lines = f.readlines()
    return {'{}'.format(line.split('\t')[1].replace('\n','')): line.split('\t')[0] for line in lines}


def load_pn_m3_dict():
    with codecs.open('./pn.csv.m3.120408.trim', 'r') as f:
        lines = f.readlines()
    return {'{}'.format(line.split('\t')[0]): line.split('\t')[1] for line in lines}


def count_pojinega(tokens, dic):

    results = {'p': 0, 'e': 0, 'n': 0}
    for token in tokens:
        if token.part_of_speech.split(',')[0] in ['動詞', '名詞', '形容詞', '副詞']:
            try:
                results[dic[token.surface]] = results[dic[token.surface]] + 1
                print(token.surface, dic[token.surface])
            except:
                continue
    return results


def all_posinega(tokens):
    posinega = get_pn_scores(tokens, load_pn_dict())
    s = sum(posinega)
    N = len(posinega)
    mean = s / N
    count = Counter(count_pojinega(tokens, load_wago_dict())) + Counter(count_pojinega(tokens, load_pn_m3_dict()))
    return mean, count