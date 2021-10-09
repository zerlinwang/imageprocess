import cv2
import numpy as np
import math

from numpy.typing import _128Bit


def rotation(origin_img, rotation_degree):
    ori_h, ori_w, ori_c = origin_img.shape
    angle = -rotation_degree * math.pi / 180
    tar_h = int(ori_w*abs(np.sin(angle)) + ori_h*abs(np.cos(angle))) + 1
    tar_w = int(ori_w*abs(np.cos(angle)) + ori_h*abs(np.sin(angle))) + 1
    target_img = np.zeros((tar_h, tar_w, 3), dtype=np.uint8)
    # set rotation matrix
    rot_mat1 = np.array([[1, 0, 0], [0, -1, 0], [-0.5*tar_w, 0.5*tar_h, 1]])
    rot_mat2 = np.array([[np.cos(angle),np.sin(angle),0],[-np.sin(angle),np.cos(angle),0],[0,0,1]])
    rot_mat3 = np.array([[1, 0, 0], [0, -1, 0],[0.5*ori_w, 0.5*ori_h, 1]])
    rot_mat = rot_mat1.dot(rot_mat2).dot(rot_mat3)

    # start rotation
    for x in range(tar_w):
        for y in range(tar_h):
            ori_point = np.array([x,y,1]).dot(rot_mat)
            if ori_point[0] >= 0 and ori_point[0] <= ori_w and ori_point[1] >= 0 and ori_point[1] <= ori_h:
                int_x = int(ori_point[0])
                int_y = int(ori_point[1])
                if int_x < ori_w-1 and int_y < ori_h-1:
                    x_ = ori_point[0] - int_x
                    y_ = ori_point[1] - int_y
                    target_img[y, x] = origin_img[int_y, int_x]*(1-x_)*(1-y_)+origin_img[int_y+1, int_x]*(1-x_)*y_+origin_img[int_y, int_x+1]*x_*(1-y_)+origin_img[int_y+1, int_x+1]*x_*y_
    return target_img

if  __name__ == '__main__':
    origin_img = cv2.imread('./tsukuba-left.bmp')
    cv2.imshow('origin_img', origin_img)
    target_img = rotation(origin_img, 40)
    cv2.imwrite('rotation_result.png', target_img)
    cv2.imshow('target_img', target_img)
    cv2.waitKey()
