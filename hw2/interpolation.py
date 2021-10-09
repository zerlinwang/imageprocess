import cv2
import numpy as np


def bilinear_interpolation(origin_img, *size):
    target_h, target_w = size
    target_img = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    print(origin_img.shape)
    origin_h, origin_w, origin_c = origin_img.shape
    if target_h == origin_h and target_w == origin_w:
        return origin_img
    for i in range(target_h):
        for j in range(target_w):
            # find corresponding point in original image
            x = j*(origin_w)/target_w
            y = i*(origin_h)/target_h
            int_x = int(x)
            int_y = int(y)
            if int_x < origin_w-1 and int_y < origin_h-1:
                x_ = x - int_x
                y_ = y - int_y
                target_img[i, j] = origin_img[int_y, int_x]*(1-x_)*(1-y_)+origin_img[int_y+1, int_x]*(1-x_)*y_+origin_img[int_y, int_x+1]*x_*(1-y_)+origin_img[int_y+1, int_x+1]*x_*y_
    return target_img

if __name__ == '__main__':
    origin_img = cv2.imread('tsukuba-left.bmp')
    cv2.imshow('origin_img', origin_img)
    target_img = bilinear_interpolation(origin_img, 864, 1152)
    cv2.imshow('target_img', target_img)
    cv2.imwrite('interpolation_result.png', target_img)
    cv2.waitKey()
