# -*- coding:utf-8 -*-

import pymongo
from core import config
import libs.tool


class MInfo(object):
    def __init__(self, cityid):
        con = pymongo.Connection('localhost')
        self.db = con['jdhby']
        self.db.authenticate('bk', 'b131322')
        self.tab_info = self.db['jdhby_{0}'.format(cityid)]

    def __disable_sig__(self, def_uid, sig):
        '''
        取消某字段的真值，变为假值
        :param def_uid:
        :param sig:
        :return:
        '''
        self.tab_info.update({'def_uid': def_uid}, {"$set": {sig: 0}})

    def get_user_jianli(self, userid):
        condition = {'userid': userid,
                     'parentid': '0900',
                     'def_valid': 1,
                     'def_banned': 0}
        db_data = self.tab_info.find(condition)
        return (db_data)

    def set_valid(self, def_uid):
        '''
        将某消息设置为有效信息
        :param def_uid:
        :return:
        '''
        # tt = self.get_by_id(def_uid)
        # tt[sig] = 0

        # {"name": "mike"}, {"$set": {"active_time": "20130408120000"}}
        try:
            self.tab_info.update({'def_uid': def_uid},
                                 {"$set": {'def_valid': 1}})
            return True
        except:
            return False

    def dis_tuiguang(self, def_uid):
        self.__disable_sig__(def_uid, 'def_tuiguang')


    def update_view_count(self, def_uid):
        views_vka = self.get_by_id(def_uid)['views']
        self.tab_info.update({'def_uid': def_uid},
                             {"$set": {'views': views_vka + 1}})

    def update_jianli(self, def_uid, new_jl_id):
        timestamp_dvi = libs.tool.get_timestamp()
        info = self.get_by_id(def_uid)
        newinfo = self.get_by_id(new_jl_id)
        # 首先判断是不是已经有这个key
        if 'def_jianli' in info:
            jianlis = info['def_jianli']
        else:
            jianlis = []
        # 再判断简单的ID是不是已经在里面了。

        for rec in jianlis:
            if new_jl_id == rec['jluid']:
                uu = jianlis.index(rec)
                jianlis.pop(uu)

        var_jl_dic = {'jluid': new_jl_id,
                      'jltitle': newinfo['title'][0],
                      'jlname': newinfo['contact_who'][0],
                      'jltime': timestamp_dvi,
                      'jlphone': newinfo['tel'][0],
                      'jlqq': newinfo['qq'][0],
                      'jltimestr': libs.tool.get_time_str(timestamp_dvi)

        }
        jianlis.insert(0, var_jl_dic)



        # jianlis= sorted(jianlis.keys(), lambda x, y: cmp(x[1], y[1]), reverse = True)

        self.tab_info.update({'def_uid': def_uid}, {"$set": {'def_jianli': jianlis}})

    def dis_zhiding(self, def_uid):
        self.__disable_sig__(def_uid, 'def_zhiding')

    def dis_fresh(self, def_uid):
        self.__disable_sig__(def_uid, 'def_refresh')


    def delete_by_uid(self, def_uid):
        self.tab_info.remove({'def_uid': def_uid})  # delet records where id = 1

    def get_list_zhiding(self, condition):
        '''
        得到置顶的记录
        '''
        # print(condition)
        db_data_out = []
        # 排序顺序：置顶、推广、更新时间
        self.sort_condition = [('def_zhiding', pymongo.DESCENDING),
                               ('def_tuiguang', pymongo.DESCENDING),
                               ('def_update_time', pymongo.DESCENDING)
        ]
        # 选择算法，得到结果
        # 首先是置顶
        # 因为置顶是固定的，所以不计算置顶的。

        condition_zhiding = condition.copy()
        condition_zhiding['def_zhiding'] = 1
        db_data = self.tab_info.find(condition_zhiding).limit(2).skip(0).sort(
            [('def_zhiding_out_time', pymongo.DESCENDING)])
        for x in db_data:
            db_data_out.append(x)

        for x in db_data:
            db_data_out.append(x)
        return (db_data_out)

    def get_list(self, condition):
        # print(condition)
        db_data_out = []
        # 排序顺序：置顶、推广、更新时间
        self.sort_condition = [('def_zhiding', pymongo.DESCENDING),
                               ('def_tuiguang', pymongo.DESCENDING),
                               ('def_update_time', pymongo.DESCENDING)
        ]
        # 选择算法，得到结果
        # # 首先是置顶
        # 因为置顶是固定的，所以不计算置顶的。
        '''
        condition_zhiding = condition.copy()
        condition_zhiding['def_zhiding'] = 1
        db_data = self.minfo.find(condition_zhiding).sort([('def_zhiding_out_time', pymongo.DESCENDING)])
        for x in db_data:
            db_data_out.append(x)
        '''

        # 然后是推广
        condition_tuiguang = condition.copy()
        condition_tuiguang['def_tuiguang'] = 1
        condition_tuiguang['def_zhiding'] = 0
        db_data = self.tab_info.find(condition_tuiguang).sort([('def_tuiguang_out_time', pymongo.DESCENDING)])
        for x in db_data:
            db_data_out.append(x)
        # print('-' * 20)

        # 然后是根据刷新来处理。
        condition_refresh = condition.copy()
        condition_refresh['def_refresh'] = 1
        condition_refresh['def_tuiguang'] = 0
        condition_refresh['def_zhiding'] = 0

        db_data = self.tab_info.find(condition_refresh).sort([('def_refresh_out_time', pymongo.DESCENDING)])
        for x in db_data:
            db_data_out.append(x)

        return (db_data_out)

    def get_list_fenye(self, condition, page_num):
        # 置顶
        zhiding_list = self.get_list_zhiding(condition)
        # 所有的记录
        all_list = self.get_list(condition)
        # 当前分页的记录
        current_list = all_list[(page_num - 1) * config.info_list_per_page: (page_num ) * config.info_list_per_page]
        return (zhiding_list + current_list)

    def get_cat_recs_count(self, catid):
        '''
        获取某一分类下的数目
        '''
        condition = {'catid': catid, 'def_valid': 1,
                     'def_banned': 0}
        condition["$or"] = [{'def_refresh': 1},
                            {'def_zhiding': 1},
                            {'def_tuiguang': 1}]
        db_data = self.tab_info.find(condition)
        return db_data.count()

    def get_by_id(self, input):
        # find a record by query
        return self.tab_info.find_one({'def_uid': input})

    def get_by_userid(self, input):
        # find a record by query
        return self.tab_info.find({'userid': input})

    def get_by_condition(self, input):
        # find a record by query
        return self.tab_info.find(input).sort([('def_refresh_out_time', pymongo.DESCENDING)])

    def get_num_condition(self, con):
        return self.tab_info.find(con).count()

    def insert_data(self, post_data):
        # 防止插入相同 UID的信息，
        # 需要先进行判断
        if self.get_by_id(post_data['def_uid']) is None:
            pass
        else:
            return False
        try:
            self.tab_info.save(post_data)
            return True
        except:
            return False


    def update(self, uid, post_data):
        try:
            self.tab_info.update({"def_uid": uid}, post_data)
            return True
        except:
            return False

    def update_user(self, uid):

        self.tab_info.update({"uid": uid}, {'userid': 'giser'})

    def clear_all(self):
        self.tab_info.remove()

    def get_all(self):
        return  self.tab_info.find()

def clear_all():
    # uu = MInfo('tonghua')
    # uu.clear_all()
    # uu = MInfo('jilin')
    # uu.clear_all()
    uu = MInfo('changchun')
    uu.clear_all()


if __name__ == '__main__':
    pass
    clear_all()

    # uu = MInfo('changchun')
    #
    # for x in uu.get_all():
    #     try:
    #         print(x['uid'])
    #         uu.update_user(x['uid'])
    #     except:
    #         pass

