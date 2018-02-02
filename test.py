import codecs
from janome.tokenizer import Tokenizer

class JanomeUtil():
    def __init__(self):
        self.t = Tokenizer()

    def get_tokens(self, txt):
        return [token for token in self.t.tokenize(txt) if token.reading is not '*']



def load_pn_dict():
    dic = {}

    with codecs.open('./pn_ja.dic', 'r', 'shift_jis') as f:
        lines = f.readlines()
    return {'{}'.format(line.split(':')[0]): float(line.split(':')[3]) for line in lines}
    
def get_pn_scores(tokens, pn_dic):
    scores = []

    for surface in [t.surface for t in tokens if t.part_of_speech.split(',')[0] in ['動詞', '名刺', '形容詞', '副詞']]:
        try:
            scores.append(pn_dic[surface])
        except:
            continue
    return scores
