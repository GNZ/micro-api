import cv2
import numpy
from matplotlib import pyplot as plt
from skimage import morphology
from skimage import exposure
from skimage.filters import sobel


class ImageAnalysis:
    def analyse(self, image_id):
        image = cv2.imread('../../images/input/blood_100x.jpg')

        if image is None:
            print('File not found')
            return

        image = cv2.medianBlur(image, 5)

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        kernel = numpy.ones((5, 5), numpy.uint8)
        gray = cv2.erode(gray, kernel)
        gray = cv2.dilate(gray, kernel)

        # Remove black border
        # _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        # removed_black = numpy.bitwise_or(gray, thresh)

        # Adaptive thresh
        gray_res = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)

        # gray = exposure.equalize_hist(gray)
        cv2.imwrite('gray.jpg', gray)

        elevation_map = sobel(gray)

        markers = numpy.zeros_like(gray)
        markers[gray < 30] = 128
        markers[gray > 150] = 255

        segmentation = morphology.watershed(elevation_map, markers)

        markers_dil = cv2.dilate(markers, kernel)

        # Work over HSV

        image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        image_h = cv2.extractChannel(image_hsv, 2)

        images = [
            ['Grayscale', gray],
            ['Elevation', elevation_map],
            ['Gray thres', gray_res],
            ['Markers', markers],
            ['Watershed seg', segmentation]
        ]

        len_i = len(images)
        for i in range(0, len_i):
            plt.subplot(2, 3, i + 1), plt.imshow(images[i][1], 'gray')
            plt.title(images[i][0])
            plt.xticks([]), plt.yticks([])
            cv2.imwrite(images[i][0] + '.jpg', images[i][1])

        plt.show()


if __name__ == '__main__':
    ia = ImageAnalysis()

    ia.analyse('blood23')
