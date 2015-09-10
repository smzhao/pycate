import os
from PIL import Image
from core import config
import libs.tool


__all__ = ['upload_imgfile']
# water_opt = 'rightlow'

dst_w = 500
dst_h = 600
water_opt = 'rightlow'

def upload_imgfile(file_dict, shuiyin=''):
    # Todo: 文件上传应该有异常处理
    # print(file_dict)
    timestamp_str = str(libs.tool.get_timestamp())
    tpname = file_dict["filename"]
    qian, hou = os.path.splitext(tpname)

    filename = libs.tool.md5(str(tpname + timestamp_str))

    img_base_dir = config.img_base_dir
    img_out_dir = os.path.join(img_base_dir, 'upload', filename[:2])
    if os.path.exists(img_out_dir):
        pass
    else:
        os.mkdir(img_out_dir)
    tpimg1 = os.path.join(img_out_dir, 'tp1' + filename + hou)
    tpimg2 = os.path.join(img_out_dir, 'tp2' + filename + hou)
    outfile = os.path.join(img_out_dir, filename + hou)
    with open(tpimg1, 'wb') as f:
        f.write(file_dict["body"])

    clipResizeImg(ori_img=tpimg1, dst_img=tpimg2, dst_w=dst_w, dst_h=dst_h)

    waterMark(ori_img=tpimg2, dst_img=outfile, mark_img=config.mark_img, water_opt=water_opt)
    # os.remove(tpimg1)
    # os.remove(tpimg2)

    return (outfile[len(img_base_dir):])


# coding:utf-8
'''
    python图片处理
    @author:fc_lamp
    @blog:http://fc-lamp.blog.163.com/
'''

# 等比例压缩图片
def resizeImg(**args):
    args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': ''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w  # 正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth, newHeight), Image.ANTIALIAS).save(arg['dst_img'])

    '''
    image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''


# 裁剪压缩图片
def clipResizeImg(**args):
    '''
    :param args:
     ori_img: 原始影像
     dst_img: 目标影像
     dst_w: 目标的宽度
     dst_h: 目标的高度
    :return:
    '''
    args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': ''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size

    dst_scale = float(arg['dst_h']) / arg['dst_w']  # 目标高宽比
    ori_scale = float(ori_h) / ori_w  # 原高宽比

    if ori_scale >= dst_scale:
        # 过高
        width = ori_w
        height = int(width * dst_scale)

        x = 0
        y = (ori_h - height) / 3

    else:
        # 过宽
        height = ori_h
        width = int(height * dst_scale)

        x = (ori_w - width) / 2
        y = 0

    # 裁剪
    box = (int(x), int(y), int(width + x), int(height + y))
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    #压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth, newHeight), Image.ANTIALIAS).save(arg['dst_img'])
    # return(True)


# 水印(这里仅为图片水印)
def waterMark(**args):
    '''
    为图片加水印
    :param args:
    :return:
    '''
    args_key = {'ori_img': '', 'dst_img': '', 'mark_img': '', 'water_opt': ''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size

    mark_im = Image.open(arg['mark_img'])
    mark_w, mark_h = mark_im.size
    option = {'leftup': (0, 0),
              'rightup': (ori_w - mark_w, 0),
              'leftlow': (0, ori_h - mark_h),
              'rightlow': (ori_w - mark_w, ori_h - mark_h),
    }

    im.paste(mark_im, option[arg['water_opt']], mark_im.convert('RGBA'))
    im.save(arg['dst_img'])


if __name__ == '__main__':
    #实例
    #原图
    ori_img = '/opt/jiheying/static/fixed/zhanwei.png'
    #水印标
    # mark_img = '/opt/jiheying/static/fixed/mark.png'
    #水印位置
    water_opt = 'rightlow'  #右下
    #生成后的目标图（保存位置）
    dst_img = ori_img + '_mark.png'
    dst_w = 200
    dst_h = 200
    #裁剪压缩
    clipResizeImg(ori_img=ori_img, dst_img=dst_img, dst_w=dst_w, dst_h=dst_h)
    #等比例压缩
    # resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h)
    #水印
    # waterMark(ori_img=ori_img,dst_img=dst_img,mark_img=mark_img,water_opt=water_opt)