import os
from html_dic import *
from array_listinfo import *
from func_to_html_listinfo import *





def do_for_dir(html_tpl):
    var_names = globals().copy().keys()
    out_dir = os.path.join(os.getcwd(), '../../templates/infolist')
    # out_dir = os.getcwd()
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    for var_name in var_names:
        if var_name.startswith('tlist_'):
            outfile = os.path.join(out_dir, 'info' + var_name[1:] + '.html')
            html_view_str_arr = []
            tview_var = eval(var_name)
            for x in tview_var:
                sig = eval('html_' + x)
                if sig['type'] == 'select':
                    html_view_str_arr.append(gen_select_view(sig))
                elif sig['type'] == 'radio':
                    html_view_str_arr.append(gen_radio_view(sig))
                elif sig['type'] == 'checkbox':
                    html_view_str_arr.append(gen_checkbox_view(sig))

            with open(outfile, 'w') as outfileo:
                outfileo.write(html_tpl.replace('xxxxxx', ''.join(html_view_str_arr)))


if __name__ == '__main__':
    str_html_tpl = open('tpl_listinfo.html').read()
    do_for_dir(str_html_tpl)
