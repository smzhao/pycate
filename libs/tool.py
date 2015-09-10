__author__ = 'bukun'
# __all__ = ['get_uid', 'md5','get_timestamp', 'get_time_str', 'markit']

import uuid
import hashlib
import time

def get_uid():
    return( str(uuid.uuid1()))

def md5(instr):
    # if type(instr) is bytes:
    m = hashlib.md5()
    m.update(instr.encode('utf-8'))
    return m.hexdigest()


def get_timestamp():
    return (int(time.time()))


def get_time_str(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return (str(otherStyleTime))


def mark_it():
    print('=' * 20)

def gen_pager(catalog_slug, total_page_num, current_page_num):
    if total_page_num == 1:
        return ''

    pager_shouye = '''
    <br/>
    <ul class="yiiPager">
    <li class="first {0} ">
    <a href="/{1}/1">&lt;&lt; 首页</a>
                </li>'''.format( 'hidden' if current_page_num <= 1 else '', catalog_slug)

    pager_pre = '''
                <li class="previous {0}"><a href="/{1}/{2}" class="previous">&lt; 前页</a>
                </li>
                '''.format('hidden' if current_page_num <= 1 else '', catalog_slug, current_page_num - 1)
    pager_mid = ''
    for ind in range(0, total_page_num):
        tmp_mid = '''
                <li class="page {0}"><a href="/{1}/{2}" class="page">{2}</a></li>
                '''.format('selected' if ind+1 == current_page_num else '', catalog_slug, ind + 1)
        pager_mid += tmp_mid
    pager_next = '''
                <li class="next {0}"><a href="/{1}/{2}" class="page">后页 &gt;</a>
                </li>
                '''.format('hidden' if current_page_num >= total_page_num else '', catalog_slug, current_page_num + 1)
    pager_last = '''
                <li class="last {0}"><a href="/{1}/{2}" >末页
                    &gt;&gt;</a>
                </li></ul>
                '''.format('hidden' if current_page_num >= total_page_num else '', catalog_slug, total_page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return(pager)