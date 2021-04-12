import cv2
import os
from PIL import Image
from PIL import ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True

def scale(pic_original, fx, fy):
    pic_result = cv2.resize(pic_original, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
    return pic_result


def main():
    val_lab_dir = 'F:/temp/tile3/labels/val/'
    fy = 0.5
    dir_new = r"F:\\temp\\tile3\\images\\train2\\"  # 缩放后图片存放的位置
    if not os.path.exists(dir_new):
        os.makedirs(dir_new)
    dir_old = r"F:\\temp\\tile3\\images\\train\\"  # 原始图片文件夹位置
    img_list = os.listdir(dir_old)
    w = 640
    h = w
    img_num = 1
    # print(img_list)

    for img_ in img_list:
        img = Image.open(dir_old + img_)
        # print(img.size)
        iw, ih = img.size

        if max(iw, ih) > 640:
            scale = min(w / iw, w / ih)
            nw = int(iw * scale)
            nh = int(ih * scale)
            new_image = img.resize((nw, nh), Image.BICUBIC)
            # new_image = Image.new('RGB', (w, h), (128, 128, 128))
            #
            # new_image.paste(img, ((w - nw) // 2, (h - nh) // 2))
            img_dir_new = os.path.join(dir_new, img_)
            new_image.save(img_dir_new)
            print("No.%d %s reshaped" %(img_num,img_))
            img_num += 1
            f_txt = open(os.path.join(lab_dir), 'w')
            f_txt.write("%s %s %s %s %s\n" % (data[i]["category"], box[0], box[1], box[2], box[3]))

if __name__ == "__main__":
    main()

# image = Image.open("")
# iw, ih = image.size
# scale = min(w / iw, w / ih)  # w,h为目标尺寸，主要先把最长的边压缩为目标尺寸然后求出缩放比
# nw = int(iw * scale)
# nh = int(ih * scale)
# image = image.resize((nw, nw), Image.BICUBIC)  # 将图片进行尺寸调整
# new_image = Image.new('RGB', (608, 608), (128, 128, 128))  # 空白补灰色
#
# new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
