# -*- coding:utf-8 -*-
# 分类
import peewee
from core.base_model import BaseModel


class phpmps_category(BaseModel):
    # id = peewee.IntegerField(null=True)
    catid = peewee.CharField(max_length=4, null=False, unique=True, help_text='类别的ID', primary_key=True)
    catname = peewee.CharField(max_length=32, null=False, help_text='类别中文名称')
    parentid = peewee.CharField(max_length=4, null=False, )
    catorder = peewee.IntegerField()
    weight = peewee.IntegerField()


class MCatalog():
    def __init__(self):
        try:
            phpmps_category.create_table()
        except:
            pass

    def getall(self):
        return phpmps_category.select()  # .order_by('catid')

    def initial_db(self, post_data):
        entry = phpmps_category.create(
            name=post_data['name'],
            id_cat=post_data['id_cat'],
            slug=post_data['slug'],
            order=post_data['order'],
        )

    def get_parent_list(self):
        db_data = phpmps_category.select().where(phpmps_category.catid == phpmps_category.parentid).order_by(
            phpmps_category.catid)
        return (db_data)

    def get_range2_with_parent(self, parentid):
        db_data = phpmps_category.select().where(phpmps_category.parentid == parentid).order_by(phpmps_category.catid)

        return (db_data)

    def get_qian2(self, qian2):
        '''
        用于首页。根据前两位，找到所有的大类与小类。
        并为方便使用，使用数组的形式返回。
        :param qian2: 分类id的前两位
        :return: 数组，包含了找到的分类
        '''

        parentid = qian2 + '00'
        a = phpmps_category.select().where(phpmps_category.parentid == parentid).order_by(phpmps_category.catid)
        return (a)

    def get_by_id(self, input):
        a = phpmps_category.get(catid=input)
        return (a)

    def get_range2_without_parent(self, parentid):
        a = phpmps_category.select().where(
            (phpmps_category.parentid == parentid) & (phpmps_category.catid != phpmps_category.parentid))
        return (a)

    def get_weight_id(self, catid):
        a = phpmps_category.get(phpmps_category.catid == catid)
        return (a.weight)

    def initial_db2(self):
        entry = phpmps_category.create(parentid='0100', catname='房屋交易', catid='0100', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='二手房出售', catid='0101', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='求购房', catid='0102', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='新房出售', catid='0103', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='出租房', catid='0104', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='合租房', catid='0105', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='短租房/日租房', catid='0106', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='求租房', catid='0107', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='商铺出租/出售', catid='0108', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='旺铺出兑', catid='0109', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='旺铺求兑/求售/求租', catid='0110', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='写字楼出租/求租', catid='0111', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0100', catname='厂房/仓库/土地', catid='0112', catorder=1, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='生活服务', catid='0200', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='搬家', catid='0201', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='家政', catid='0202', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='租赁 租车', catid='0203', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='婚庆 摄影', catid='0204', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='家具维修/开锁', catid='0205', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='鲜花/庆典', catid='0206', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='送水/订餐', catid='0207', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='粮油批发', catid='0208', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='起名/易测', catid='0209', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='节日礼品', catid='0210', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0200', catname='食品油水批发', catid='0211', catorder=2, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='车辆与服务', catid='0300', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='汽车出售/转让', catid='0301', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='准新车', catid='0302', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='求购车', catid='0303', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='摩托车出售/求购', catid='0304', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='自行车/电动车/求购', catid='0305', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='驾校/租车/代驾/陪练', catid='0306', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='救援车/抢修车', catid='0307', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='拼车/顺风车', catid='0308', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='修车行/4S店/配件', catid='0309', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='汽车用品/装饰', catid='0310', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='货车/工程车/农用车', catid='0311', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0300', catname='过户上牌/年检', catid='0312', catorder=3, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='商业服务', catid='0400', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='金融/担保贷款', catid='0401', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='招商加盟', catid='0402', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='公司注册/年检', catid='0403', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='会计/审计/评估', catid='0404', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='快递/物流', catid='0405', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='装修/建材', catid='0406', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='网站建设', catid='0407', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='设计策划', catid='0408', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='网络维护/电脑维修', catid='0409', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='法律咨询/商标注册', catid='0410', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='印刷/包装', catid='0411', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='喷绘招聘/制卡', catid='0412', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='工装服务', catid='0413', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0400', catname='清欠/商务调查', catid='0414', catorder=4, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='跳蚤市场', catid='0500', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='台式电脑', catid='0501', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='二手笔记本', catid='0502', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='平板电脑', catid='0503', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='手机买卖', catid='0504', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='电子数码产品', catid='0505', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='手机号码专区', catid='0506', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='二手家具', catid='0507', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='超级回收', catid='0508', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='求购/置换/租赁', catid='0509', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='艺术/工艺/收藏品', catid='0510', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='母婴/儿童用品', catid='0511', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='服饰/箱包/鞋帽/手表', catid='0512', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='门票卡券', catid='0513', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0500', catname='其他物品', catid='0514', catorder=5, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='交友征婚', catid='0600', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='帅哥美女', catid='0601', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='男士征婚', catid='0602', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='女士征婚', catid='0603', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='同性别交友', catid='0604', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='同乡会', catid='0605', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='兴趣交友', catid='0606', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='真情告白/祝福', catid='0607', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='寻人寻友', catid='0608', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0600', catname='技能交换', catid='0609', catorder=6, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='人才招聘', catid='0700', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='销售/业务', catid='0701', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='客服/话务/营业员', catid='0702', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='文员/内勤/助理/翻译', catid='0703', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='人事/行政/后勤/采购', catid='0704', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='出纳/财务/收银/库管', catid='0705', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='前台/迎宾/导游', catid='0706', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='房产经纪人', catid='0707', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='保险行业', catid='0708', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='各种车辆司机', catid='0709', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='汽车维修/装饰行业', catid='0710', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='厨师餐饮行业', catid='0711', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='教育培新行业', catid='0712', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='家政服务行业', catid='0713', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='医疗健康行业', catid='0714', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='计算机/网络/电子商务', catid='0715', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='建筑/装修/物业/保安', catid='0716', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='娱乐行业', catid='0717', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='美容美发行业', catid='0718', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='印刷/喷绘/广告传媒行业', catid='0719', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='工厂技术/机械制造行业', catid='0720', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0700', catname='兼职/临促/终点/实习', catid='0721', catorder=7, weight=5, )
        entry = phpmps_category.create(parentid='0800', catname='医疗健康', catid='0800', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='0800', catname='男科疾病', catid='0801', catorder=8, weight=5, )
        entry = phpmps_category.create(parentid='0800', catname='妇科疾病', catid='0802', catorder=8, weight=5, )
        entry = phpmps_category.create(parentid='0800', catname='找医院/自诊自查', catid='0803', catorder=8, weight=5, )
        entry = phpmps_category.create(parentid='0800', catname='养生/健康', catid='0804', catorder=8, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='求职简历', catid='0900', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='销售', catid='0901', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='客服', catid='0902', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='人事/行政/后勤', catid='0903', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='酒店/餐饮', catid='0904', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='美容/美发/保健/健身', catid='0905', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='计算机/网络/通信', catid='0906', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='建筑/房产/装修/物业', catid='0907', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='普工/技工/生产', catid='0908', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='司机', catid='0909', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='家政保洁/安保', catid='0910', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='影视/娱乐/KTV', catid='0911', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='编辑/出版/印刷', catid='0912', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='教育培训/翻译', catid='0913', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='财务/审计/统计', catid='0914', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='护士/医生', catid='0915', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='资料员', catid='0916', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='营业员', catid='0917', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='演艺/影视', catid='0918', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='0900', catname='其他职位', catid='0919', catorder=9, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='同城活动', catid='1000', catorder=0, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='团购/打折', catid='1001', catorder=10, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='商城特价', catid='1002', catorder=10, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='餐饮美食', catid='1003', catorder=10, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='旅游度假', catid='1004', catorder=10, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='酒店/宾馆', catid='1005', catorder=10, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='休闲娱乐', catid='1006', catorder=10, weight=5, )
        entry = phpmps_category.create(parentid='1000', catname='美容/美体/运动', catid='1007', catorder=10, weight=5, )


if __name__ == '__main__':
    uu = MCatalog()
    tt = uu.getall()
    for x in tt:
        print(x.catid)
