import os
import json
import cv2 as cv


def reshape(img, output_size, iw, ih):
    global t
    w = output_size
    h = output_size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)
    src = cv.resize(img, (nw, nh))
    newImg = cv.copyMakeBorder(src, (640 - nh) // 2, (640 - nh) // 2, (640 - nw) // 2, (640 - nw) // 2,
                               cv.BORDER_CONSTANT, None)
    if (w / iw) < (h / ih):
        wb = 1 - 2 * t / iw
        hb = scale - 2 * t / output_size
    else:
        wb = scale - 2 * t / output_size
        hb = 1 - 2 * t / ih
    return newImg, wb, hb

    # img_dir_new = os.path.join(newImg, img_)
    # newImg.save(img_dir_new)
    # print("No.%d %s reshaped" % (img_num, img_))


def cut_img(img, bbox):
    global t
    wth = bbox[2] - bbox[0]
    hth = bbox[3] - bbox[1]
    img = cv.copyMakeBorder(img, 640, 640, 640, 640, cv.BORDER_CONSTANT, None)
    if 0 < max(wth, hth) <= 640:
        nx1 = int(640 + bbox[0] - 0.5 * (640 - wth))
        nx2 = nx1 + 640
        ny1 = int(640 + bbox[1] - 0.5 * (640 - hth))
        ny2 = ny1 + 640
        region = img[ny1: ny2, nx1: nx2]
        wb = wth / 640
        hb = hth / 640
    else:

        region = img[int(bbox[1] + 640) - t:int(bbox[3] + 640) + t, int(bbox[0] + 640 - t):int(bbox[2] + 640) + t]
        ih, iw = -(int(bbox[1]) - int(bbox[3])) + 2 * t, -(int(bbox[0] - t) - (int(bbox[2]) + t))
        region, wb, hb = reshape(region, 640, iw, ih)

    ax, ay = 0.5, 0.5
    new_box = (ax, ay, wb, hb)
    return region, new_box


# ImageFile.LOAD_TRUNCATED_IMAGES = True

old_img_dir = 'F:/pytorch/tile_round1_train_20201231/train_imgs/'
vals_xml_dir = 'F:/pytorch/tile_round1_train_20201231/train_annos.json'
train_lab_dir = 'F:/temp/tile3/labels/train/'
train_img_dir = 'F:/temp/tile3/images/train/'
val_lab_dir = 'F:/temp/tile3/labels/val/'
val_img_dir = 'F:/temp/tile3/images/val/'

t = 40

data = json.load(open(vals_xml_dir, 'r'))
print(len(data))

for i in range(len(data)):
    print(i)
    old_box = data[i]["bbox"]
    if max(old_box[2] - old_box[0], old_box[3] - old_box[1]) <= 640:
        continue
    # im_size = (data[i]["image_height"], data[i]["image_width"])
    # print(img["file_name"])
    old_img = cv.imread(old_img_dir + data[i]["name"])
    new_img, box = cut_img(old_img, data[i]["bbox"])
    j = i
    if i <= 10000:
        img_dir = train_img_dir + "000" + '%d' % j + ".jpg"
        lab_dir = train_lab_dir + "000" + '%d' % j + ".txt"
    else:
        img_dir = val_img_dir + "000" + '%d' % j + ".jpg"
        lab_dir = val_lab_dir + "000" + '%d' % j + ".txt"
    cv.imwrite(img_dir, new_img)
    f_txt = open(os.path.join(lab_dir), 'w')
    f_txt.write("%s %s %s %s %s\n" % (data[i]["category"], box[0], box[1], box[2], box[3]))
