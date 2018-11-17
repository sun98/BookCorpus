"""
@Author: Sun Suibin
@Date: 2018-11-17 12:17:08
@Last Modified by: Sun Suibin
@Last Modified time: 2018-11-17 12:17:08
"""
import json
import os

from bs4 import BeautifulSoup as bs

import import_helper
from config import BOOK_DIR, BOOK_SA_DIR, DATA_DIR, CHAPTER_DIR


def seperate(soup_list):
    cpt_names = []
    chapters = []
    soup_list.reverse()
    cpt_count, tmp_cpt, cpt_seq, new = 0, [], [], False
    cpt_name = []
    for ind, soup in enumerate(soup_list):
        if soup.name == 'p':
            if new:
                cpt_text = '\n'.join(tmp_cpt)
                if len(tmp_cpt) > 5 and len(cpt_text) > 1000:
                    chapters.insert(0, cpt_text)
                    if len(cpt_name) == 1:
                        cpt_names.insert(0, cpt_name[0].strip())
                    else:
                        cpt_name_string = ''
                        for name in cpt_name:
                            if 'chapter' not in name.lower() and len(name) > 5:
                                cpt_name_string += (name + ' ')
                        cpt_names.insert(0, cpt_name_string.strip())
                    tmp_cpt = []
                    cpt_count += 1
                    new = False
                    cpt_name = []
                else:
                    tmp_cpt = []
                    new = False
            tmp_cpt.insert(0, soup.text.strip())
        else:
            if ind == 0:
                continue
            if cpt_count == 0:
                cpt_seq.insert(0, soup.name)
                new = True
                cpt_name.insert(0, soup.text.strip())
            else:
                if soup.name not in cpt_seq:
                    continue
                else:
                    new = True
                    cpt_name.insert(0, soup.text.strip())
                    if ind == len(soup_list) - 1:
                        cpt_text = '\n'.join(tmp_cpt)
                        if len(tmp_cpt) > 5 and len(cpt_text) > 1000:
                            chapters.insert(0, cpt_text)
                            if len(cpt_name) == 1:
                                cpt_names.insert(0, cpt_name[0].strip())
                            else:
                                cpt_name_string = ''
                                for name in cpt_name:
                                    if 'chapter' not in name.lower() and len(name) > 5:
                                        cpt_name_string += (name + ' ')
                                cpt_names.insert(0, cpt_name_string.strip())
                            tmp_cpt = []
                            cpt_count += 1
                            new = False
                            cpt_name = []

    return cpt_names, chapters


def get_main(soup):
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'p']
    main_list = []
    old_name = ''
    pre = soup.pre
    if pre is None:
        return []
    for element in pre.next_siblings:
        if element.name in tags:
            main_list.append(element)
            # if element.name == old_name:
            #     print(',' + element.name, end='')
            # else:
            #     print('\n' + element.name, end='')
            # old_name = element.name
    # print()
    return main_list


def slicer(_file):
    print(f'slicing {_file}')
    encodings = ['utf-8', 'ISO-8859-1', 'ISO-8859-2']
    for e in encodings:
        with open(_file, 'r', encoding=e) as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                if e == 'ISO-8859-2':
                    raise Exception(f'no encoding way for {_file}')
                continue
    soup = bs(content, features="lxml").body
    soup_list = get_main(soup)
    if len(soup_list) == 0:
        print(f'{_file} failed')
        return
    cpt_names, chapters = seperate(soup_list)
    if len(cpt_names) <= 1:
        print(f'{_file} failed')
        return
    filename = os.path.join(CHAPTER_DIR, os.path.splitext(os.path.basename(_file))[0][1:] + '.json')
    content = {}
    for ind in range(len(cpt_names)):
        # print(cpt_names[ind])
        # print(chapters[ind][:20], '\t', chapters[ind][-20:], '\n')
        content[ind] = {
            'cpt_name': cpt_names[ind],
            'cpt_text': chapters[ind]
        }
    json.dump(content, open(filename, 'w'), indent=2)


def filter_book_list(tag_file, new_tag_file):
    print(f'start filtering book list')
    keywords = ['fiction', 'satire', 'stories', 'story', 'history', 'tale']
    filtered_tag = {}
    tags = json.load(open(tag_file, 'r'))
    for book in tags:
        info = tags[book]
        subject = info['subject']
        for keyword in keywords:
            if keyword in subject:
                filtered_tag[book] = info
                break
    print(f'totally {len(filtered_tag)} books')
    json.dump(filtered_tag, open(new_tag_file, 'w'), indent=2)


if __name__ == '__main__':
    # filter_book_list(os.path.join(DATA_DIR, 'tag.json'), os.path.join(DATA_DIR, 'tag_filtered.json'))
    sample_dir = BOOK_DIR
    tag_file = os.path.join(DATA_DIR, 'tag_filtered.json')
    blacklist = os.path.join(DATA_DIR, 'blacklist.json')

    sample_books = [f'f{x}.html' for x in json.load(open(tag_file, 'r'))][:]
    black_books = json.load(open(blacklist, 'r'))
    for book in sample_books:
        if book not in black_books:
            slicer(os.path.join(sample_dir, book))
        # break
    pass
