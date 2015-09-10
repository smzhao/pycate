# -*- coding:utf-8 -*-
import peewee

from core.base_model import BaseModel


class phpmps_city(BaseModel):
    cityid = peewee.CharField(max_length=32, null=False, unique=True, help_text='类别的ID', primary_key=True)
    cityname = peewee.CharField(max_length=32, null=False, help_text='类别中文名称')
    parentid = peewee.CharField(max_length=4, null=False, )
    ordr = peewee.IntegerField()


class MCity(BaseModel):
    def __init__(self):
        try:
            phpmps_city.create_table()
            pass
        except:
            pass

    def getall(self):
        return (phpmps_city.select().order_by(phpmps_city.ordr))

    def get_cityname_by_id(self, par_cityid):
        return (phpmps_city.get(cityid=par_cityid).cityname)


if __name__ == '__main__':
    uu = MCity()
    print(uu.getall())
