import nltk
import text_input
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
import re
from nltk.stem.wordnet import WordNetLemmatizer
import collections
import math
import time

def isNoise(token):
    min_token_length = 2
    is_noise = True
    if re.match(r'^NN', token.tag_):
        #or re.match(r'^RB', token.tag_) or token.tag_ == 'JJ':
        is_noise = False
    
    if token.is_stop:
        is_noise = True
    if len(token.string) <= min_token_length:
        is_noise = True
    return is_noise


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

def cleanup(token, tokenizer, lower=True):
    if lower:
        token = token.lower()
    return ''.join(tokenizer.tokenize(token.strip()))

def text_handler_v2(nlp, text):
    #t = time.time()
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    # nlp = spacy.load("en")
    # text = text_input.test_para_input()
    text = text.replace('\n', ' ')  # 去换行符
    text = text.lower()  # 大写换小写
    # print(time.time() - t)
    # print("%%%")
    #t = time.time()
    
    doc = nlp(text)
    
    cleaned_list = [(cleanup(word.lemma_, tokenizer)) for word in doc if not isNoise(word)]
    # print(cleaned_list)
    # print(time.time() - t)
    # print("%%%")
    # t = time.time()
    # for item in cleaned_list0:
    #     print(item)
    # labels = [(w, w.label_) for w in document.ents]
    # for item in cleaned_list:
    #     print(item)
    return word_count_v2(cleaned_list)

def text_handler_v3():
    # for item in doc.noun_chunks:
    #     print(item.text, item.root.dep_)
    pass


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


def word_count_v2(text):
    # print(text)
    
    c = collections.Counter(text)
    result = {}
    for letter, count in c.most_common():  # 提取数量前五
        result[letter] = count
    # for key, item in result.items():
    #     print(key, item)
    return result


def cal_tf_idf(count_set):
    temp_dir = {}
    r = []
    for cpt in count_set:
        for word in cpt.keys():
            count = 0
            if word not in temp_dir.keys():
                for inner_cpt in count_set:
                    if word in inner_cpt.keys():
                        count += 1
                temp_dir[word] = count
            else:
                count = temp_dir[word]
            cpt[word] = math.log((len(count_set) / count), math.e) * cpt[word]
    for item in count_set:
        # print(sorted(item.items(), key=lambda x: x[1], reverse=True)[0:5])
        r.append(sorted(item.items(), key=lambda x: x[1], reverse=True)[0:4])
    
    return r
