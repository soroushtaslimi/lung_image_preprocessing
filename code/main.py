import glob
import os
import numpy as np
import cv2
from typing import Tuple

data_path = '../data/images_001'
result_path = '../Results/images_001'
dilation_size = (91, 91)


def find_contour_of_point(contours, point):
    for contour in contours:
        if cv2.pointPolygonTest(contour, point, False) == 1:
            return contour
    return None


def find_nearest_contour(contours, point):
    max_dist = -float('inf')
    selected_contour = None
    for contour in contours:
        dist = cv2.pointPolygonTest(contour, point, True)
        if dist > max_dist:
            max_dist = dist
            selected_contour = contour
    return selected_contour


def dilated_bounding_box(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return max(0, x-dilation_size[0]), max(0, y-dilation_size[1]), w + 2*dilation_size[0], h + 2*dilation_size[1]


if __name__ == '__main__':
    filelist = glob.glob(os.path.join(data_path, '*'))
    
    for file_name in filelist:
        image_gray = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
        # image_gray = image_gray[int(1/8*image_gray.shape[0]):int(7/8*image_gray.shape[0]), int(1/8*image_gray.shape[1]):int(7/8*image_gray.shape[1])]
        # print(image_gray.shape)
        mean_brightness = np.mean(image_gray)
        custom_range = (1, mean_brightness)
        
        print('mean_pixels(image):', mean_brightness)
        
        im_bw = 255 - cv2.threshold(image_gray, int(mean_brightness), 255, cv2.THRESH_BINARY)[1]
        
        
        kernel = np.ones(dilation_size, dtype=np.uint8)
        im_bw = cv2.erode(im_bw, kernel, iterations=1)
        
        contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        left_point = (int((3*image_gray.shape[0]/5)//2), image_gray.shape[1]//2)
        right_point = (int((7*image_gray.shape[0]/5)//2), image_gray.shape[1]//2)
        
        left_contour = find_nearest_contour(contours, left_point)
        right_contour = find_nearest_contour(contours, right_point)
                
        im_bgr = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(im_bgr, [left_contour, right_contour], -1, (0,255,0), 3)
        
        xl, yl, wl, hl = dilated_bounding_box(left_contour)
        xr, yr, wr, hr = dilated_bounding_box(right_contour)
        
        cv2.rectangle(im_bgr,(xl,yl),(xl+wl,yl+hl),(200,0,0),2)
        cv2.rectangle(im_bgr,(xr,yr),(xr+wr,yr+hr),(200,0,0),2)
        
        # cv2.imshow('draw contours',im_bgr)
        # cv2.waitKey(0)
        cv2.imwrite(os.path.join(result_path, os.path.basename(file_name)), im_bgr)
