import json
import multiprocessing as mp
import os

import import_helper
import text_ana
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


def book_dir_cont(item):
    with open(os.path.join(input_dir, item), 'r') as file:
        book = json.load(file)
    # pool.apply_async(self.book_dir_cont, args=book)

    # book_dir = self.book_dir_cont(book)
    book_dir = {}

    for key, value in book.items():
        cpt_dir = {}
        cpt_name = value['cpt_name']
        result = text_ana.text_handler_v1(value['cpt_text'])
        # result = text_ana.word_count(handled_text)
        cpt_dir['cpt_name'] = cpt_name
        cpt_dir['cpt_key'] = result
        # print(result)
        book_dir[key] = cpt_dir

    with open(os.path.join(output_dir, item), "w") as outfile:
        json.dump(book_dir, outfile, indent=2)
        print(f"{item} done")

    # return book_dir


if __name__ == '__main__':
    book_mp()
    pass
