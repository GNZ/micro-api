import cv2
import numpy
from matplotlib import pyplot as plt
from skimage import morphology
from skimage import exposure
from skimage.color import label2rgb
from skimage.filters import rank
from skimage.filters import sobel
from scipy import ndimage as ndi
from skimage.morphology import disk


class ImageAnalysis:
    def analyse(self, image_id):
        image = cv2.imread('../../images/input/blood_100x.jpg')

        numpy.set_printoptions(threshold='nan')

        if image is None:
            print('File not found')
            return

        # image = cv2.medianBlur(image, 5)

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        kernel = numpy.ones((5, 5), numpy.uint8)
        # gray = cv2.erode(gray, kernel)
        #gray = cv2.dilate(gray, kernel)

        gray = exposure.equalize_adapthist(gray)

        for i in range(0, len(gray)):
            for j in range(0, len(gray[0])):
                gray[i, j] *= 255

        # output = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        #cv2.imwrite('gray.jpg', output)

        elevation_map = sobel(gray)
        # elevation_map = ndi.distance_transform_cdt(gray)

        gray = gray.astype(int)

        #print gray

        markers = numpy.zeros_like(gray)
        markers[gray < 80] = 2  # seen as white in plot
        markers[gray > 200] = 1  # seen as black in plot

        #print markers

        segmentation = morphology.watershed(elevation_map, markers)

        print segmentation

        segmentation = ndi.binary_fill_holes(segmentation - 1)

        labeled_coins, _ = ndi.label(segmentation)
        image_label_overlay = label2rgb(labeled_coins, image=image)

        print 'labeled coins '
        #print labeled_coins

        images = [
            ['Grayscale', gray],
            ['Elevation', elevation_map],
            ['Markers', markers],
            ['Watershed seg', segmentation]
        ]

        len_i = len(images)
        for i in range(0, len_i):
            plt.subplot(2, 3, i + 1), plt.imshow(images[i][1], 'gray')
            plt.title(images[i][0])
            plt.xticks([]), plt.yticks([])
            # cv2.imwrite(images[i][0] + '.jpg', images[i][1])

        plt.subplot(2, 3, 5), plt.imshow(image_label_overlay)

        plt.show()


if __name__ == '__main__':
    ia = ImageAnalysis()

    ia.analyse('blood23')
