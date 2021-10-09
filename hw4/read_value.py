import numpy as np
import cv2

if __name__ == '__main__':
    img = cv2.imread('A.bmp')
    print(img[50:100, 50:100, 0])