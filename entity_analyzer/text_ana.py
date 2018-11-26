import nltk
import text_input
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
import re
from nltk.stem.wordnet import WordNetLemmatizer
import collections


def contain_english(str0):
    import re
    return bool(re.search('[a-z]', str0))


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''


def isv_isn(word):
    return re.match(r'NN*', word) or re.match(r'VB', word)


def text_handler_v1(text):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    lmtzr = WordNetLemmatizer()
    # print(text)

    text = text.replace('\n', ' ')  # 去换行符

    text = text.lower()  # 大写换小写
    # print(text)

    sentences = nltk.sent_tokenize(text)  # 分句

    sentences = [nltk.word_tokenize(sent) for sent in sentences]  # 分词

    sentences = [[w for w in sent_list if w not in stopwords.words('english')] for sent_list in sentences]  # 去停词
    # for ind, sent_list in sentences:
    #     sentences[ind] = [w for w in sent_list if w not in stopwords.words('english')]
    # print(sentences)

    sentences = [nltk.pos_tag(sent) for sent in sentences]  # 标注词性
    # print(sentences)

    sentences = [[word for word in sent if isv_isn(word[1])] for sent in sentences]  # 过滤掉非名词和非动词'
    # for ind, sent in sentences:
    #     sentences[ind] = [word for word in sent if isv_isn(word[0])]
    # print(sentences)

    sentences = [[word for word in sent if (contain_english(str(word[0])) and len(word[0]) != 0)] for sent in
                 sentences]  # 过滤只有标点却被标注为名词和动词的元素
    # for ind, sent in sentences:
    #     sentences[ind] = [word for word in sent if (contain_english(str(word[0])) and len(word[0]) != 0)]

    sentences = [[(word[0], get_wordnet_pos(word[1])) for word in sent] for sent in sentences]  # 获得词干前词性对应
    # for ind, sent in sentences:
    #     sentences[ind] = [(word[0], get_wordnet_pos(word[1])) for word in sent]

    sentences = [[lmtzr.lemmatize(word[0], word[1]) for word in sent] for sent in sentences]  # 词干提取
    # for ind, sent in sentences:
    #     sentences[ind] = [lmtzr.lemmatize(word[0], word[1]) for word in sent]

    # for item in sentences:
    #     #print(item)

    sentences = [[' '.join(tokenizer.tokenize(word)) for word in sent] for sent in sentences]  # 去文字中标点
    # print(sentences)
    return word_count(sentences)


def word_count(text):
    new_text = []
    for item in text:
        new_text.extend(item)
    c = collections.Counter(new_text)
    result = {}
    for letter, count in c.most_common(5):  # 提取数量前五
        result[letter] = count
    # print(result)
    return result
# word_count(text_handler())
