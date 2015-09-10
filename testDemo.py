import sys
import os
sys.path.append(os.getcwd())

import requests

from libs import upload

#实例
#原图
ori_img = '/opt/jihy/jihy_src/static/fixed/zhanwei.png'
#水印标
mark_img = '/opt/jihy/jihy_src/static/fixed/mark.png'
#水印位置
water_opt = 'rightlow' #右下
#生成后的目标图（保存位置）
dst_img = ori_img + '_mark.png'
dst_w = 100
dst_h = 80
#裁剪压缩
upload.clipResizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h)
#等比例压缩
# upload.resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h)
#水印
# upload.waterMark(ori_img=ori_img,dst_img=dst_img,mark_img=mark_img,water_opt=water_opt)