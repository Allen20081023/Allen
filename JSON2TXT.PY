
from __future__ import print_function
import os, sys, zipfile
import json


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2]-box[0]
    h = box[3]-box[1]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


json_file = 'F:/pytorch/tile_round1_train_20201231/train_annos.json'  # # Object Instance 类型的标注

data = json.load(open(json_file, 'r'))

ana_txt_save_path = "./val"  # 保存的路径
if not os.path.exists(ana_txt_save_path):
    os.makedirs(ana_txt_save_path)
print(len(data))

for i in range(len(data)):
    # print(img["file_name"])
    filename = data[i]["name"]
    img_width = data[i]["image_width"]
    img_height = data[i]["image_height"]
    # print(img["height"])
    # print(img["width"])
    # img_id = img["id"]
    ana_txt_name = filename.split(".")[0] + ".txt"  # 对应的txt名字，与jpg一致
    print(ana_txt_name)
    f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')
    # for ann in data[i]['category']:
    #     if ann['name'] == filename:
            # annotation.append(ann)
            # print(ann["category_id"], ann["bbox"])
    box = convert((img_width, img_height), data[i]["bbox"])
    f_txt.write("%s %s %s %s %s\n" % (data[i]["category"], box[0], box[1], box[2], box[3]))

# ————————————————
# 版权声明：本文为CSDN博主「ZongHaoFan」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/fanzonghao/article/details/93753826