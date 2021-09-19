import numpy as np
from skimage import color
from skimage.io import imread, imsave
import pandas as pd


class ImageTransformer:
    def __init__(self, path_to_image, illness_name, path_to_tables):
        self.name = illness_name
        self.image = imread(path_to_image)
        self.table = pd.read_csv(path_to_tables + illness_name + ".csv")

    def find_nearest(self, pixel):
        tmp1 = pixel[2] // 16
        tmp2 = pixel[1] // 16
        tmp3 = pixel[0] // 16
        index = tmp1 + 16 * tmp2 + 16 * 16 * tmp3
        return np.array(self.table.iloc[index, 3:])

    def transform(self):
        if self.name == "monochromacy":
            self.image = color.rgb2gray(self.image)
        else:
            cache = {}
            for i in range(self.image.shape[0]):
                for j in range(self.image.shape[1]):
                    curr_pixel = self.image[i][j]
                    curr_pixel_rgb = tuple(map(int, tuple(curr_pixel)))
                    if curr_pixel_rgb in cache:
                        self.image[i][j] = cache[curr_pixel_rgb]
                    else:
                        new_color = self.find_nearest(curr_pixel)
                        self.image[i][j] = new_color
                        cache[curr_pixel_rgb] = new_color

    def get_image(self):
        return self.image


path_to_image = input()
path_to_save = input()
path_to_tables = input()
illness_name = input()
img = ImageTransformer(path_to_image, illness_name, path_to_tables)
img.transform()
new_img = img.get_image()
imsave(path_to_save, new_img)
