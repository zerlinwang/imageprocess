import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import _256Bit


def histogram_equal(img):
    NUM = 256
    h, w, c = img.shape
    assert c == 3
    color_dist = np.array([[0]*NUM for i in range(c)])
    # Statistical image grayscale distribution
    for i in range(h):
        for j in range(w):
            for k in range(c):
                color_dist[k][img[i][j][k]] += 1
    # plt.bar(range(NUM), color_dist[0])
    # Cal the CDF
    cdf = np.array([[0]*NUM for i in range(c)])
    cdf[0][0] = color_dist[0][0]
    cdf[1][0] = color_dist[1][0]
    cdf[2][0] = color_dist[2][0]
    for i in range(1, NUM):
        for j in range(c):
            cdf[j][i] = color_dist[j][i] + cdf[j][i-1]
    # Histogram equalization
    result = np.zeros((h,w,c), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            for k in range(c):
                result[i][j][k] = round((cdf[k][img[i][j][k]] - cdf[k][0])/(cdf[k][NUM-1]-cdf[k][0])*(NUM-1))
    # plt.bar(range(NUM), color_dist_[0])
    plt.hist(img.reshape(h*w*c,), bins=range(NUM))
    plt.show()
    plt.hist(result.reshape(h*w*c,), bins=range(NUM))
    plt.show()
    # plt.savefig('c_hist.png')
    # cv2.imwrite('c_processed.bmp', result)
    return result


if __name__ == '__main__':
    # image_a = cv2.imread('a.bmp')
    # image_b = cv2.imread('b.bmp')
    image_c = cv2.imread('c.bmp')
    # result_img_a = histogram_equal(image_a)
    # result_img_b = histogram_equal(image_b)
    result_img_c = histogram_equal(image_c)
    # cv2.imshow('original image a', image_a)
    # cv2.imshow('original image b', image_b)
    # cv2.imshow('original image c', image_c)
    # cv2.imshow('result_image a', result_img_a)
    # cv2.imshow('result_image b', result_img_b)
    # cv2.imshow('result_image c', result_img_c)
    cv2.waitKey()
