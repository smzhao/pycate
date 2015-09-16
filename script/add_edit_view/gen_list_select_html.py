import os
from html_dic import *
from array_list import *


def to_html(bl_str):
    bianliang = eval(bl_str)
    html_out = '''
    <div class="row" style="line-height:30px;">

    <div class="col-sm-2">{0}</div>
    <div class="col-sm-10"> <span class="label label-default"  name='{1}' onclick='change(this);'  value=''>全部</span>
    '''.format(bianliang['zh'], bl_str.split('_')[1])

    tmp_dic = bianliang['dic']
    for key in tmp_dic.keys():
        tmp_str = '''<span  class="label label-default"  name='{0}' onclick='change(this);' value='{1}'>{2}</span>
    '''.format(bl_str.split('_')[1], key, tmp_dic[key])
        html_out += tmp_str
    html_out += '''</div></div>'''
    return (html_out)


def do_for_dir(html_tpl):
    var_names = globals().copy().keys()
    out_dir = os.path.join(os.getcwd(), '../../templates/list')
    # out_dir = os.getcwd()
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    for var_name in var_names:
        if var_name.startswith('tlist_'):
            outfile = os.path.join(out_dir, var_name[1:] + '.html')
            html_view_str_arr = []
            tview_var = eval(var_name)
            for x in tview_var:
                html_view_str_arr.append(to_html('html_' + x))

            with open(outfile, 'w') as outfileo:
                outfileo.write(html_tpl.replace('xxxxxx', ''.join(html_view_str_arr)))


if __name__ == '__main__':
    str_html_tpl = open('tpl_list.tpl').read()
    do_for_dir(str_html_tpl)
