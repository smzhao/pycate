# -*- coding:utf-8 -*-
def gen_input_add(sig):
    html_fangjia = '''
    <div class="form-group">
    <label for='{0}'><span style="color:red">*</span>{1}</label>
    <input id='{0}' name="{0}" value="" type="text" style="width:350px" class="number"> {2}
    </div>'''.format( sig['en'], sig['zh'], sig['dic'][1])
    return (html_fangjia)

def gen_input_edit(sig):
    edit_fangjia = '''
    <div class="form-group">
    <label for='{0}'><span style="color:red">*</span>{1}</label>
    <input id='{0}' name="{0}" value="{{{{ post_info['{0}'][0] }}}}" type="text" style="width:350px" class="number"> {2}
    </div>'''.format( sig['en'], sig['zh'], sig['dic'][1])
    return (edit_fangjia)

def gen_input_view(sig):
    out_str = '''
    <div class="pure-u-1-4 iga_view_rec"><span class="des">{1}</span></div>
    <div class="pure-u-3-4 iga_view_rec"><span class="val">{{{{ post_info['{0}'][0] }}}} {2}</span></div>
    ''' .format(sig['en'],sig['zh'], sig['dic'][1])
    return (out_str)


def gen_radio_add(sig):
    html_zuoxiang = '''
    <div class="form-group">
    <label for="{0}"><span style="color:red">*</span>{1}</label>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="radio" class="required" value="{1}">{2}
        '''.format(sig['en'], key, dic_tmp[key])
        html_zuoxiang += tmp_str

    html_zuoxiang += '''</div>'''
    return (html_zuoxiang)

def gen_radio_edit(sig):
    edit_zuoxiang = '''
    <div class="form-group">
    <label for="{0}"><span style="color:red">*</span>{1}</label>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="radio" class="required" value="{1}"
        {{% if post_info['{0}'][0] == '{1}' %}}
        checked
        {{% end %}}
        >{2}'''.format(sig['en'], key, dic_tmp[key])
        edit_zuoxiang += tmp_str

    edit_zuoxiang += '''</div>'''
    return (edit_zuoxiang)

def gen_radio_view(sig):
    view_zuoxiang = '''
    <div class="pure-u-1-4 iga_view_rec"><span class="des">{0}</span></div>
    <div class="pure-u-3-4 iga_view_rec">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span class="val">
         {{% if post_info['{0}'][0] == "{1}" %}}
         {2}
         {{% end %}}
         </span>
        '''.format(sig['en'], key, dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return (view_zuoxiang)



def gen_checkbox_add(sig):
    html_wuneisheshi = '''
    <div class="form-group">
    <label for="{0}"><span style="color:red">*</span>{1}</label>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="checkbox" class="required" value="{1}">{2}
        '''.format(sig['en'], key, dic_tmp[key])
        html_wuneisheshi += tmp_str

    html_wuneisheshi += '''</div>'''
    return (html_wuneisheshi)
def gen_checkbox_edit(sig):
     edit_wuneisheshi = '''
     <div class="form-group">
     <label for="{0}"><span style="color:red">*</span>{1}</label>
     '''.format(sig['en'], sig['zh'])

     dic_tmp = sig['dic']
     for key in dic_tmp.keys():
         tmp_str = '''
         <input id="{0}" name="{0}" type="checkbox" class="required" value="{1}"
         {{% if "{1}" in post_info["{0}"] %}}
         checked="checked"
         {{% end %}}
         >{2}'''.format( sig['en'], key, dic_tmp[key])
         edit_wuneisheshi += tmp_str

     edit_wuneisheshi += '''</div>'''
     return (edit_wuneisheshi)
def gen_checkbox_view(sig):
    view_zuoxiang = '''
    <div class="pure-u-1-4 iga_view_rec"><span class="des">{0}</span></div>
    <div class="pure-u-3-4 iga_view_rec">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span class="val">
         {{% if "{0}" in post_info["{1}"] %}}
         {2}
         {{% end %}}
         </span>
         '''.format( key, sig['en'], dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return (view_zuoxiang)

def gen_select_add(sig):
    html_jushi = '''
    <div class="form-group">
    <label for="{0}"><span style="color:red">*</span>{1}</label>
    <select id="{0}" name="{0}" class="required">
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']

    for key in dic_tmp.keys():
        tmp_str = '''
        <option value="{1}">{2}</option>
        '''.format(sig['en'], key, dic_tmp[key])
        html_jushi += tmp_str

    html_jushi += '''</select></div>'''
    return (html_jushi)

def gen_select_edit(sig):
    edit_jushi = '''
    <div class="form-group">
    <label for="{0}"><span style="color:red">*</span>{1}</label>
    <select id="{0}" name="{0}" class="required">
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''        
        <option value="{1}"
        {{% if post_info["{0}"][0] == "{1}" %}}
        selected = "selected"
        {{% end %}}
        >{2}</option>        
        '''.format(sig['en'], key, dic_tmp[key])
        edit_jushi += tmp_str

    edit_jushi += '''</select></div>'''
    return (edit_jushi)

def gen_select_view(sig):
    view_jushi = '''
    <div class="pure-u-1-4 iga_view_rec"><span class="des">{0}</span></div>
    <div class="pure-u-3-4 iga_view_rec">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span class="val">
          {{% set tmp_var = post_info["{0}"][0] %}}
          {{% if tmp_var == "{1}" %}}
          {2}
          {{% end %}}
         </span>
         '''.format(sig['en'], key, dic_tmp[key])
        view_jushi += tmp_str

    view_jushi += '''</div>'''
    return (view_jushi)



def gen_file_add(sig):
    add_html = '''
    <div class="form-group">
    <label for="dasf">上传图片：</label>
    <label id="dasf" style="width:400px;"><span style="margin-left:20px;">png,jpg,gif,jpeg格式！大小不得超过500KB</span></label>
    </div>
    <div class="form-group">
    <label for="mymps_img2"> </label>
    <label id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img1">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img3">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img4">
    </label>
    </div>
    '''
    return(add_html)

def gen_file_view(sig):
    view_html = ''
    return(view_html)

def gen_file_edit(sig):
    view_html = '''
    <div class="form-group">
    <label for="dasf">上传图片：</label>
    <label id="dasf" style="width:500px;text-align:left;"><span style="margin-left:5px; width:500px;">png,jpg,gif,jpeg格式！大小不得超过500KB</span></label>
    </div>
    <div class="form-group">
    <label for="mymps_img2"> </label>
    <label id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img1">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img3">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img4">
    </label>
    </div>
    '''
    return(view_html)
