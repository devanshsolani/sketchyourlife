'''
BSD 3-Clause License

Copyright (c) 2020, Tauhid Khan, Devyesh Thomas
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import numpy as np
from numpy import ndarray
from cv2 import filter2D, imwrite
from PIL import Image, UnidentifiedImageError

import os


class ImageProcess:
    '''
    TODO change all variable of the class to private members
    Main class for implementing some Image processing and image minipulation

    Algorithm implemented:
            TODO to implement Average and Lens Blurr
            -Image blur/smooth
                +Gaussian blur/smooth
                +Average blurr
                +lens blurr
            TODO to implement image resizing
            -Image Resize
                +Bicubic
                +Bilinear
            -Image converting to Grayscale
            -Image inverting
            -Image Blendding
                +color dodge
            -Image Padding
    '''

    def __init__(self):
        pass

    # Some utils functions

    def _rotate_image_90(self, img: ndarray, k: int) -> ndarray:
        """
        TODO to implement image rotation without using np.rot90()

        Rotates the image if the img.shape[0]<img.shape[1] 
        i.e height is less than width as PIL.Image.open() 
        reads image the as [h,w,c]

        args:
            img - [ndarray] an image of type np.ndarray
            k - [int] Integer to define the number of time 
                to rotate image 90 degree i.e k*90 degree

        returns:
            img - [ndarray] an rotated image of type np.ndarray
        """
        if img.shape[0] < img.shape[1]:
            self.y = np.rot90(img, k)
            return self.y
        else:
            return img

    def _gaussian_distribution(self, x: ndarray, mu: float, sigma: float) -> ndarray:
        """
        It returns the gassian distribution of the given ndarray

        args:
            [x] - [ndarray] 
            mu - [float] mean of the gaussian distribution
            sigma - [float] standard deviation of the gaussian distribution

        return:
            ndarray - Gaussian distribution of the given x ndarray with
            standard deviation sigma and mean mu
        """
        return 1 / (np.sqrt(2 * np.pi) * sigma) * np.exp(
            -np.power(
                (x - mu) / sigma, 2) / 2)

    def _generate_gaussian_kernel(self, size: int, sigma: float = 1.0, mu: float = 0.0) -> ndarray:
        """
        Generate gaussian kernel of given given size and dims (sizexsize)

        args:
            size - [int] deifnes the size of the kernel (sizexsize)
            sigma - [float] standard diviation of gaussian
                    distribution. It cannot be 0.0
            mu - [float] mean of the gaussian distribution

        return:
            kernel2D - [ndarray] gaussian kernel the values are in range (0,1)
        """
        # create the 1D array of equally spaced distance point of given size
        self.kernel_1d = np.linspace(-(size//2), size//2, size)
        # get the gaussian distribution of the 1D array
        self.kernel_1d = self._gaussian_distribution(
            self.kernel_1d, mu, sigma)

        # Compute the outer product of kernel1D tranpose and kernel1D
        self.kernel_2d = np.outer(self.kernel_1d.T, self.kernel_1d)
        # normalize the the outer product to suish the values between 0.0-1.0
        self.kernel_2d *= 1.0/self.kernel_2d.max()
        return self.kernel_2d

    def _pad_image(self, img: ndarray, pad_width: int = 10) -> ndarray:
        """
        TODO to implement padding for RGB images.

        NOTE: Currently it can pad only grayscale image only

        Pads the image from all side with zeros.

        args:
            img - [ndarray] image to padded
            pad_width - [int] width of the pad around the image

        return:
            padded_img - [ndarray] image with padding around
        """
        self.padded_img = np.zeros(
            (img.shape[0] + pad_width*2, img.shape[1]+pad_width*2))
        self.padded_img[pad_width:-pad_width, pad_width:-pad_width] = img
        return self.padded_img

    def _normalize_img(self, img: ndarray, range_end: float = 1.0) -> ndarray:
        """
        NOTE: range should be > 0.0

        Normalize the image pixel values in range (0,range_range).

        args:
            img - [ndarray] input image to be normalized.
            range_end -[float] 

        return:
            img - [ndarray] normalized image
        """
        return (img/img.max())*range_end

    def _isGrayscale(self, img: ndarray) -> bool:
        """
        Checks if image is grayscale or not

        arg:
            img - [ndarray] image to check

        return
            bool 
        """
        if len(np.squeeze(img).shape) == 2:
            return True
        else:
            return False
    # main functions

    def loadImage(self, path: str) -> ndarray:
        """
        reads the image from the path and returns a numpy array

        args:
            [path] - str

        returns:
            [img] numpy.ndarray with shape [h,w,c](for RGB channels) 
            or (h,w,1)(for grayscale image)
        """
        try:
            self.img = np.asarray(Image.open(path))

        except FileNotFoundError:

            print("NO such File {}".format(path))
            return None
        return self.img

    def saveImage(self, img: ndarray, path: str, name: str) -> bool:
        self.__isSaved = imwrite(os.path.join(path, name), img)
        return self.__isSaved

    def RGB2GRAY(self, img: ndarray) -> ndarray:
        """
        Converts a RGB image to Grayscale image

        args:
            img - [ndarray] image that to be converted to grayscale

        return:
            img - [ndarray] Converted grayscale image

        """
        # checks if the image is already in grayscale format
        if self._isGrayscale(img):
            return img
        else:
            self.rgb_weights = np.array([0.2126, 0.7152, 0.0722])
            return np.dot(img[..., :3], self.rgb_weights)

    def invertImage(self, img: ndarray) -> ndarray:
        """
        Inverts an image

        args:
            img - [ndarray] image that to be inverted

        return:
            img - [ndarray] inverted image
        """
        return img.max() - img

    def naiveConvolve2D(self, img: ndarray, kernel: ndarray) -> ndarray:
        """
        TODO:to implement fater version of the convolution operatration 
            and add striding to downsample image

        NOTE:It is a naive approach to convolve image with kernel.

        Convolves image with the given kernel

        args:
            img - [ndarray] input image
            kernel - [ndarray] kernel of any size

        return:
            convolved2d - [ndarray] a convolved
        """
        self.kernel_size = kernel.shape[0]
        self.convolved_output = np.zeros_like(img)

        self.padded_image = self._pad_image(img, pad_width=self.kernel_size-2)

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                self.convolved_output[y, x] = (
                    kernel * self.padded_image[y:y+self.kernel_size, x:x+self.kernel_size]).sum()

        return self.convolved_output

    def gaussianBlur(self, img: ndarray, kernel_size: int = 21, sigma: float = 10.0) -> ndarray:
        """
        NOTE: For now we use cv2.filter2d and not naiveConvolve2d to speed up computation

        Apply gaussian blurr on given image

        args:
            img - [ndarray] Image to be blurred
            kernel_size - [int] size of the kernel (sizexsize)
            sigma - [float] standard deviation for gaussian distribution

        return:
            blurred_img - [ndarray] blurred image 
        """
        if not isinstance(img, ndarray):
            raise "image should be in form of np.ndarray"

        self.__kernel = self._generate_gaussian_kernel(kernel_size, sigma)
        self.__blurrImg = filter2D(img, -1, self.__kernel)
        self.__blurrImg = self._normalize_img(self.__blurrImg, range_end=255.0)
        return self.__blurrImg

    def colorDodge(self, img1: ndarray, img2: ndarray) -> ndarray:
        """
        TODO to implement different type of image blending
        It blends the image1 with image2 as background using colorDodge

        args:
            img1 - [ndarray] image 1 should be normalized within the range (0,1)
            img2 - [ndarray] image 2 should be normalized within the range (0,1)

        return:
            blended_img - [ndarray] Image1 blended with Image2x
        """
        if img1.max()>1.0 and img2.max()>1.0:
            raise "np.ndarray should be normalized within the range (0,1)"
        
        self.blended_img = img2/((1.0 - img1)+10e-12)
        self.blended_img[self.blended_img > 1.0] = 1.0
        self.blended_img = self._normalize_img(
            self.blended_img, range_end=255.0)
        return self.blended_img                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
