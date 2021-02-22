from PIL import Image, ImageFilter
import glob
import os
import numpy as np
import cv2

data_path = '../data/images_001'
result_path = '../Results/images_001_mean_erosion_dilation'
threshold = 100
# custom_range = (0, 150)
morph_kernel_size = 90


class RegionGrowing:
    def __init__(self, image, start_point, threshold=100, custom_range=None):
        self.image = image
        self.pixels = image.load()
        self.image_size = image.size
        self.start_point = start_point
        self.threshold = threshold
        if custom_range is None:
            self.accepted_range = (pixels[start_point] - threshold, pixels[start_point] + threshold)
        else:
            self.accepted_range = custom_range
    
    def get_neighbors(self, point):
        neighbors = []
        for i in [-1, 1]:
            new_x = point[0] + i
            if new_x < 0 or new_x >= self.image_size[0]:
                continue
            neighbors.append((new_x, point[1]))
        for j in [-1, 1]:
            new_y = point[1] + j
            if new_y < 0 or new_y >= self.image_size[1]:
                continue
            neighbors.append((point[0], new_y))
                
        return neighbors


    def is_similar(self, point):
        return self.accepted_range[0] <= self.pixels[point] and self.pixels[point] <= self.accepted_range[1]
        # return np.abs(self.pixels[point] - self.pixels[self.start_point]) <= self.threshold


    def find_region(self):
        checked = set()
        to_check = set()
        similar_points = set()
        to_check.add(self.start_point)
        while(to_check):
            point = to_check.pop()
            checked.add(point)
            # print(point)
            if self.is_similar(point):
                similar_points.add(point)
                for neighbor in self.get_neighbors(point):
                    if neighbor not in checked:
                        to_check.add(neighbor)
        return similar_points


def mean_pixels(image):
    sum = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            sum += image.getpixel((i, j))
    return sum/(image.size[0]*image.size[1])


# def dilate(image):
    


if __name__ == '__main__':
    filelist = glob.glob(os.path.join(data_path, '*'))
    print(filelist)
    for file_name in filelist[:1]:
        image = Image.open(file_name).convert('L')
        # print(image.size)
        mean_brightness = mean_pixels(image)
        custom_range = (1, mean_brightness)
        print('mean_pixels(image):', mean_brightness)
        start_point = (int((3*image.size[0]/5)//2), image.size[1]//2)
        # region_growing = RegionGrowing(image, start_point, threshold=threshold)
        region_growing = RegionGrowing(image, start_point, custom_range=custom_range)
        region = region_growing.find_region()
        
        pixels = image.load()
        
        """
        new_image = Image.new('L', image.size)
        for point in region:
            new_image.putpixel(point, pixels[point])
        """
        
        new_image = np.zeros(image.size)
        for point in region:
            new_image[point] = pixels[point]
        new_image = Image.fromarray(new_image.transpose().astype(np.uint8))
        """
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if pixels[i, j] > threshold:
                    pixels[i, j] = 0
        """
        
        #  dilation
        # new_image = new_image.filter(ImageFilter.MinFilter(5))
        
        kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
        # dilated_img = cv2.dilate(np.array(new_image), kernel, iterations=1)
        eroded_img = cv2.erode(np.array(new_image), kernel, iterations=1)
        
        # image = np.array(image)
        # print(image.shape)
        # print(image[image.shape[0]//2, image.shape[1]//2])
        # image.show()
        # print(os.path.basename(file_name))
        
        # cv2.imshow('Dilation', dilated_img)
        cv2.imwrite(os.path.join(result_path, os.path.basename(file_name)), eroded_img)
        
        # new_image.save(os.path.join(result_path, os.path.basename(file_name)))
        image.close()
        new_image.close()
        
        # cv2.waitKey(0)
    