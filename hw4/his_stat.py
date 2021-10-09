import cv2
import numpy as np
import copy
from numpy.core.fromnumeric import mean


def his_stat(img):
    h, w, c = img.shape
    result = copy.deepcopy(img)
    # 填充四周的像素值
    # result[0] = img[0]
    # result[h-1] = img[h-1]
    # result[:, 0] = img[:, 0]
    # result[:, w-1] = img[:, w-1]
    # 求得图像的均值和标准差
    img_mean = np.mean(img)
    img_std = np.std(img)
    # 设定系数
    k0, k1, k2, k3 = 0.15, 0.3, 0., 0.049
    img_max = np.max(img)
    # 遍历图像进行增强
    for i in range(1, h-1):
        for j in range(1, w-1):
            kernel = np.array([img[i,j],img[i-1,j-1],img[i,j-1],img[i+1,j-1],img[i-1,j],img[i+1,j],
                img[i-1,j+1],img[i,j+1],img[i+1,j+1]])
            kernel_mean = np.mean(kernel)
            kernel_std = np.std(kernel)
            kernel_max = np.max(kernel)
            coefficient = np.round(img_max/kernel_max)
            # 判断是否符合增强条件
            if k0*img_mean <= kernel_mean <= k1*img_mean and k2*img_std <= kernel_std <= k3*img_std:
                result[i, j] = coefficient * result[i, j]
    return result


if __name__ == '__main__':
    img = cv2.imread('A.bmp')
    result = his_stat(img)
    cv2.imwrite('A_enhanced.bmp', result)