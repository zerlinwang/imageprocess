import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse


def fuzzy(value):
    if value <= 63:
        dark = 1.
    elif value >= 127:
        dark = 0.
    else:
        dark = (127-value)/0.015625
    if value <= 127:
        brig = 0.
    elif value >= 191:
        brig = 1.
    else:
        brig = (value-127)/0.015625
    if value >= 191:
        gray = 0.
    elif value <= 63:
        gray = 0.
    elif value <= 127:
        gray = (value-63)/0.015625
    else:
        gray = (191-value)/0.015625
    return dark, gray, brig

def fuzzy_trans(img):
    h, w, c = img.shape
    result = np.zeros((h,w,c), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            dark, gray, brig = fuzzy(img[i,j,0])
            result[i,j] = ((dark * 0) + (gray * 127) + (brig * 255))/(dark + gray + brig)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', '-i', default='B', help='which image would you like to enhance? [B] or [C]?')
    args = parser.parse_args()
    name = args.image
    img = cv2.imread(f'{name}.bmp')
    img_hist = cv2.calcHist(img, [0], None, [256], [0,255])
    result = fuzzy_trans(img)
    result_hist = cv2.calcHist(result, [0], None, [256], [0,255])
    cv2.imshow('origin image', img)
    cv2.imshow('result image', result)
    cv2.imwrite(f'{name}_enhanced.bmp', result)
    plt.plot(img_hist)
    plt.title(f'origin {name} image hist')
    plt.savefig(f'original {name} histogram.png')
    plt.close()
    plt.plot(result_hist)
    plt.savefig(f'enhanced {name} histogram.png')
    plt.show()
    cv2.waitKey()