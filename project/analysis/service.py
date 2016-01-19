import cv2
import numpy
from scipy import ndimage as ndi
from skimage import exposure
from skimage import morphology
from skimage.filters import sobel, threshold_otsu

from project.analysis.model import Analysis
from project.util.image_utils import ImageUtils


class ImageAnalysisService:
    def __init__(self):
        self.image_utils = ImageUtils()

    def analyse(self, image_id):
        analysis = self.analysis_script(image_id)

        return analysis

    def analysis_script(self, image_id):
        analysis = Analysis(image_id)

        # Read the image
        image = cv2.imread(self.image_utils.getInputFilename(image_id))

        if image is None:
            print('File not found')
            return

        # Work on green channel
        gray = image[:, :, 1]

        thresh = threshold_otsu(gray)
        gray[gray < thresh] = 0

        gray = exposure.equalize_adapthist(gray) * 255

        elevation_map = sobel(gray)

        gray = gray.astype(int)

        markers = numpy.zeros_like(gray)
        markers[gray < 80] = 2  # seen as white in plot
        markers[gray > 200] = 1  # seen as black in plot

        # Segment with watershed using elevation map
        segmentation = morphology.watershed(elevation_map, markers)
        segmentation = ndi.binary_fill_holes(segmentation - 1)
        labeled_image, n = ndi.label(segmentation)

        # Set count
        analysis.count = n

        # Set name
        analysis.name = 'Red cell count'

        return analysis
