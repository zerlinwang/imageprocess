import cv2
import numpy as np
import argparse


def affine(tar_w, tar_h, ori_w, ori_h, matrix, result_img, origin_img):
    for x in range(tar_w):
        for y in range(tar_h):
            point = np.array([x,y,1]).dot(matrix)
            if point[0] >= 0 and point[0] <= ori_w and point[1] >= 0 and point[1] <= ori_h:
                int_x = int(point[0])
                int_y = int(point[1])
                if int_x < ori_w-1 and int_y < ori_h-1:
                    x_ = point[0] - int_x
                    y_ = point[1] - int_y
                    result_img[y, x] = origin_img[int_y, int_x]*(1-x_)*(1-y_)+origin_img[int_y+1, int_x]*(1-x_)*y_+origin_img[int_y, int_x+1]*x_*(1-y_)+origin_img[int_y+1, int_x+1]*x_*y_
    return result_img


def affine_trans(origin_img, trans_type):
    ori_w = 500
    ori_h = 500
    tar_w = 550
    tar_h = 650
    trans_matrix = np.array([[1, -0.3, 0], [-0.1, 1, 0], [0, 0, 1]])
    o2t_matrix = np.array([[1, 0, 0], [0, -1, 0], [-0.5*ori_w, 0.5*ori_h, 1]]).dot(trans_matrix).dot(np.array([[1, 0, 0], [0, -1, 0], [0.5*tar_w, 0.5*tar_h, 1]]))
    t2o_matrix = np.array([[1, 0, 0], [0, -1, 0], [-0.5*tar_w, 0.5*tar_h, 1]]).dot(np.linalg.inv(trans_matrix)).dot(np.array([[1, 0, 0], [0, -1, 0], [0.5*ori_w, 0.5*ori_h, 1]]))
    if trans_type == 'o2t':
        matrix = t2o_matrix
        result_img = np.zeros((tar_h, tar_w, 3), dtype=np.uint8)
        result_img = affine(tar_w, tar_h, ori_w, ori_h, matrix, result_img, origin_img)
        cv2.imwrite('a_ori2a_trans_result.png', result_img)
    elif trans_type == 't2o':
        matrix = o2t_matrix
        result_img = np.zeros((ori_h, ori_w, 3), dtype=np.uint8)
        result_img = affine(ori_w, ori_h, tar_w, tar_h,  matrix, result_img, origin_img)
        cv2.imwrite('a_trans2a_ori_result.png', result_img)
    else:
        raise "transform type error!"
    print(o2t_matrix, t2o_matrix)
    result_img = affine(tar_w, tar_h, ori_w, ori_h, matrix, result_img, origin_img)
    return result_img


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--transformation_type', '-tt', type=str, default='o2t', help='if you want to transform from a_ori to a_trans, please input \'o2t\', otherwise input \'t2o\'')
    args = parser.parse_args()
    trans_type = args.transformation_type
    origin_img = cv2.imread('a_ori.jpg')
    target_img = cv2.imread('a_trans.jpg')
    if trans_type == 'o2t':
        result_img = affine_trans(origin_img, 'o2t')
    else:
        result_img = affine_trans(target_img, 't2o')
    cv2.imshow('result_img', result_img)
    cv2.waitKey()
