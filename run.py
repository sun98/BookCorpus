"""
@Author: Sun Suibin
@Date: 2018-12-04 20:23:02
@Last Modified by:   Sun Suibin
@Last Modified time: 2018-12-04 20:23:02
"""

from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import BooleanField, Form, IntegerField, TextField, validators

from app.db_config import DB_HOST, DB_NAME, DB_PW, DB_USER
from app.db_query import query_book_by_name_title, query_image_by_title_cptnum, query_image_by_bookid_cpt_num, query_image_by_word, query_image_by_title_word, query_image_by_title_cpttitle

app = Flask(__name__)


class FindBookForm(Form):
    title = TextField('Find book by book title', [validators.DataRequired()])
    author = TextField('and author name', render_kw={"placeholder": "optional"})


class FindPicByBookCpt(Form):
    title = TextField('Fin image by book title', [validators.DataRequired()])
    cpt_num = IntegerField('and chapter index', render_kw={"placeholder": "optional"})


class FindPicByIdCpt(Form):
    bid = IntegerField('Fin image by book id', [validators.DataRequired()])
    cpt_num = IntegerField('and chapter index', render_kw={"placeholder": "optional"})


class FindPicByWord(Form):
    title = TextField('and book title', render_kw={"placeholder": "optional"})
    word = TextField('Fin image by key word', [validators.DataRequired()])


class FindPicByTitleCptTitle(Form):
    title = TextField('Fin image by book title', [validators.DataRequired()])
    cpt_title = TextField('and chapter title', [validators.DataRequired()])


@app.route('/', methods=['GET'])
def index():
    book_form = FindBookForm()
    pic_form1 = FindPicByBookCpt()
    pic_form2 = FindPicByIdCpt()
    pic_form3 = FindPicByWord()
    pic_form4 = FindPicByTitleCptTitle()
    # if request.method == 'POST' and book_form.validate():
    #     book_result = query_book_by_name_title(book_form.title.data, book_form.author.data)
    #     return render_template('index.html', book_form=book_form, book_result=book_result)
    return render_template('index.html', book_form=book_form, pic_form1=pic_form1, pic_form2=pic_form2, pic_form3=pic_form3, pic_form4=pic_form4)


@app.route('/book', methods=['POST'])
def book():
    book_form = FindBookForm(request.form)
    pic_form1 = FindPicByBookCpt()
    pic_form2 = FindPicByIdCpt()
    pic_form3 = FindPicByWord()
    pic_form4 = FindPicByTitleCptTitle()
    if request.method == 'POST' and book_form.validate():
        book_result = query_book_by_name_title(book_form.title.data, book_form.author.data)
        print(len(book_result))
        book_result = [list(x) for x in book_result]
        for i in range(len(book_result)):
            book_result[i][-1] = '/' + '/'.join(book_result[i][-1].replace('\\', '/').split('/')[2:])
        return render_template('index.html', book_form=book_form, book_result=book_result,
                               pic_form1=pic_form1, pic_form2=pic_form2, pic_form3=pic_form3, pic_form4=pic_form4)
    flash('输入不合法')
    return redirect('/')


@app.route('/pic1', methods=['POST'])
def pic1():
    book_form = FindBookForm()
    pic_form1 = FindPicByBookCpt(request.form)
    pic_form2 = FindPicByIdCpt()
    pic_form3 = FindPicByWord()
    pic_form4 = FindPicByTitleCptTitle()
    if request.method == 'POST' and pic_form1.validate():
        pic_result1 = query_image_by_title_cptnum(pic_form1.title.data, pic_form1.cpt_num.data)
        print(len(pic_result1))
        pic_result1 = [list(x) for x in pic_result1]
        for i in range(len(pic_result1)):
            pic_result1[i][-1] = '/' + '/'.join(pic_result1[i][-1].replace('\\', '/').split('/')[2:])
        return render_template('index.html', pic_result1=pic_result1, book_form=book_form,
                               pic_form1=pic_form1, pic_form2=pic_form2, pic_form3=pic_form3, pic_form4=pic_form4)
    flash('输入不合法')
    return redirect('/')


@app.route('/pic2', methods=['POST'])
def pic2():
    book_form = FindBookForm()
    pic_form1 = FindPicByBookCpt()
    pic_form2 = FindPicByIdCpt(request.form)
    pic_form3 = FindPicByWord()
    pic_form4 = FindPicByTitleCptTitle()
    if request.method == 'POST' and pic_form2.validate():
        pic_result2 = query_image_by_bookid_cpt_num(pic_form2.bid.data, pic_form2.cpt_num.data)
        print(len(pic_result2))
        pic_result2 = [list(x) for x in pic_result2]
        for i in range(len(pic_result2)):
            pic_result2[i][-1] = '/' + '/'.join(pic_result2[i][-1].replace('\\', '/').split('/')[2:])
        return render_template('index.html', pic_result2=pic_result2, book_form=book_form,
                               pic_form1=pic_form1, pic_form2=pic_form2, pic_form3=pic_form3, pic_form4=pic_form4)
    flash('输入不合法')
    return redirect('/')


@app.route('/pic3', methods=['POST'])
def pic3():
    book_form = FindBookForm()
    pic_form1 = FindPicByBookCpt()
    pic_form2 = FindPicByIdCpt()
    pic_form3 = FindPicByWord(request.form)
    pic_form4 = FindPicByTitleCptTitle()
    if request.method == 'POST' and pic_form3.validate():
        if pic_form3.title.data is None:
            pic_result3 = query_image_by_word(pic_form3.word.data)
        else:
            pic_result3 = query_image_by_title_word(pic_form3.title.data, pic_form3.word.data)
        print(len(pic_result3))
        pic_result3 = [list(x) for x in pic_result3]
        for i in range(len(pic_result3)):
            pic_result3[i][-1] = '/' + '/'.join(pic_result3[i][-1].replace('\\', '/').split('/')[2:])
        return render_template('index.html', pic_result3=pic_result3, book_form=book_form,
                               pic_form1=pic_form1, pic_form2=pic_form2, pic_form3=pic_form3, pic_form4=pic_form4)
    flash('输入不合法')
    return redirect('/')


@app.route('/pic4', methods=['POST'])
def pic4():
    book_form = FindBookForm()
    pic_form1 = FindPicByBookCpt()
    pic_form2 = FindPicByIdCpt()
    pic_form3 = FindPicByWord()
    pic_form4 = FindPicByTitleCptTitle(request.form)
    if request.method == 'POST' and pic_form4.validate():
        pic_result4 = query_image_by_title_cpttitle(pic_form4.title.data, pic_form4.cpt_title.data)
        print(len(pic_result4))
        pic_result4 = [list(x) for x in pic_result4]
        for i in range(len(pic_result4)):
            pic_result4[i][-1] = '/' + '/'.join(pic_result4[i][-1].replace('\\', '/').split('/')[2:])
        return render_template('index.html', pic_result4=pic_result4, book_form=book_form,
                               pic_form1=pic_form1, pic_form2=pic_form2, pic_form3=pic_form3, pic_form4=pic_form4)
    flash('输入不合法')
    return redirect('/')


if __name__ == '__main__':
    # app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_NAME}:{DB_PW}@{DB_HOST}/{DB_NAME}'
    # db = SQLAlchemy(app)
    app.run(debug=True)
