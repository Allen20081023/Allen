import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFile
from matplotlib import patches


def load_classes(path):
    with open(path, "r") as fp:
        names = fp.read().split("\n")[:-1]
    return names


if __name__ == '__main__':
    # class_path = 'F:/temp/tile3/labels/train'
    # class_list = load_classes(class_path)
    img_path = 'F:/temp/tile3/images/train/00011779.jpg'
    img = np.array(Image.open(img_path))
    H, W, C = img.shape
    label_path = 'F:/temp/tile3/labels/train/00011779.txt'
    boxes = np.loadtxt(label_path, dtype=np.float).reshape(-1, 5)
    # xywh to xxyy
    boxes[:, 1] = (boxes[:, 1] - boxes[:, 3] / 2) * W
    boxes[:, 2] = (boxes[:, 2] - boxes[:, 4] / 2) * H
    boxes[:, 3] *= W
    boxes[:, 4] *= H
    fig = plt.figure()
    ax = fig.subplots(1)
    for box in boxes:
        bbox = patches.Rectangle((box[1], box[2]), box[3], box[4], linewidth=2,
                                 edgecolor='r', facecolor="none")
        label = int(box[0])
        # Add the bbox to the plot
        ax.add_patch(bbox)
        # Add label
        plt.text(
            box[1],
            box[2],
            s=label,
            color="white",
            verticalalignment="top",
            bbox={"color": 'g', "pad": 0},
        )
        ax.imshow(img)
    plt.show()
