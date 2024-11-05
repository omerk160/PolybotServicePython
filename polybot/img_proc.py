from pathlib import Path
from matplotlib.image import imread, imsave
import random
import os
from PIL import Image, ImageFilter


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()
        self.height = len(self.data)
        self.width = len(self.data[0])

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result


    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        # One loop iterates over columns in the original image the other loops iterates overs rows reversing the order to achieve clockwise rotation
        # The image is represented as a 2D list (self.data) where self.data[i][j] refers to the intensity of the pixel at the i'th row and j'th column
        rotated_data = [[self.data[self.height - j - 1][i] for j in range(len(self.data))]
                        for i in range(len(self.data[0]))]
        self.data = rotated_data

    def salt_n_pepper(self):
        # this method adds random noise by setting some pixels to white (255) and others to black (0).
        # the probability threshholds for salt (white) are 0.2 and 0.8 for pepper (black)

        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                rand_val = random.random()
                if rand_val < 0.2:
                    self.data[i][j] = 255  # Salt (white)
                elif rand_val > 0.8:
                    self.data[i][j] = 0

    def concat(self, other_img, direction='horizontal'):
        # The concat method joins two images, self and other_img
        # Either horizontally (side-by-side) or vertically (stacked), depending on the direction argument.

        if direction == 'horizontal':
            # Ensure both images have the same height
            if len(self.data) != len(other_img.data):
                raise RuntimeError("Images must have the same height for horizontal concatenation.")

            concatenated_data = [row1 + row2 for row1, row2 in zip(self.data, other_img.data)]

        elif direction == 'vertical':
            # Ensure both images have the same width
            if len(self.data[0]) != len(other_img.data[0]):
                raise RuntimeError("Images must have the same width for vertical concatenation.")

            concatenated_data = self.data + other_img.data

        else:
            raise ValueError("Direction must be either 'horizontal' or 'vertical'.")

        self.data = concatenated_data


    def segment(self):
        # The segment method will segment the image based on intensity.
        # Pixels with an intensity above a certain threshold (100) will be set to white, while others will be set to black.
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                # Set pixel to white if above threshold, otherwise black
                self.data[i][j] = 255 if self.data[i][j] > 100 else 0