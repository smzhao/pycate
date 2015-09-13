# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import sys,os
import html2text
import tornado.escape
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer
from torlite.model.mpost import MPost

whoosh_database = 'database/whoosh'
def build_directory():
    if os.path.exists('locale'):
        pass
    else:
        os.mkdir('locale')

    if os.path.exists(whoosh_database):
        pass
    else:
        os.makedirs (whoosh_database)


def build_whoosh_database():

    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True, analyzer = analyzer), type=TEXT(stored=True), link=ID(stored=True),
                    content=TEXT(stored=True, analyzer=analyzer))
    ix = create_in(whoosh_database, schema)

    writer = ix.writer()

    mpost = MPost()
    recs = mpost.query_all()
    for rec in recs:
        text2 =  html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        print(text2)
        writer.add_document(
            title=rec.title,
            type='<span style="color:blue;">[文档]</span>',
            link='/post/{0}.html'.format(rec.uid),
            content= text2
        )
    writer.commit()

if __name__ == '__main__':
    build_directory()
    build_whoosh_database()