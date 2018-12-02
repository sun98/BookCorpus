import json
import multiprocessing as mp
import os

import import_helper
import text_ana
import spacy
import time
from config import BOOK_DIR, CHAPTER_DIR, DATA_DIR, ENTITY_DIR

input_dir = CHAPTER_DIR
output_dir = ENTITY_DIR
generated = os.listdir(output_dir)
books_list = os.listdir(input_dir)
books_list = [x for x in books_list if x not in generated]
print(len(books_list))


def book_mp():
    with mp.Pool(processes=8) as pool:
        for item in books_list:
            pool.apply_async(book_dir_cont, args=(item,))
            # break
        pool.close()
        pool.join()


def book_dir_cont(book_name):
    # t = time.time()
    with open(os.path.join(input_dir, book_name), 'r') as file:
        book = json.load(file)
    # pool.apply_async(self.book_dir_cont, args=book)
    # print(time.time() - t)
    # t = time.time()
    # book_dir = self.book_dir_cont(book)
    book_dir = {}
    book_count = []
    book_temp = []
    nlp = spacy.load("en")
    # print(time.time() - t)
    # t = time.time()
    for key, value in book.items():
        cpt_dir = {}
        cpt_name = value['cpt_name']
        temp_count = text_ana.text_handler_v2(nlp, value['cpt_text'])
        book_count.append(temp_count)
        # result = text_ana.word_count(handled_text)
        cpt_dir['cpt_name'] = cpt_name
        cpt_dir['key_name'] = key
        book_temp.append(cpt_dir)
    # print(time.time() - t)
    # t = time.time()
    book_count = text_ana.cal_tf_idf(book_count)
    # print (book_count)
    for i in range(len(book_temp)):
        book_temp[i]['cpt_key'] = book_count[i]
    for item in book_temp:
        book_dir[item['key_name']] = item
    # cpt_dir['cpt_key'] = result
    # book_dir[key] = cpt_dir
    # break
    # print(time.time() - t)
    # t = time.time()
    with open(os.path.join(output_dir, book_name), "w") as outfile:
        json.dump(book_dir, outfile, indent=2)
        print(book_name, " done")
    # print(time.time() - t)
    # t = time.time()

# return book_dir


if __name__ == '__main__':
    book_mp()
    pass
