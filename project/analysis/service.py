import cv2
import numpy
from scipy import ndimage as ndi
from skimage import exposure
from skimage import morphology
import skimage.filter
from skimage.feature import peak_local_max
from skimage.measure import regionprops

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

        # Apply otsu thresholding
        thresh = skimage.filter.threshold_otsu(gray)
        gray[gray < thresh] = 0

        # Apply histogram equalization
        gray = exposure.equalize_adapthist(gray) * 255

        # Create elevation map
        elevation_map = skimage.filter.sobel(gray)

        gray = gray.astype(int)

        # Create cell markers
        markers = numpy.zeros_like(gray)
        markers[gray < 100] = 2  # seen as white in plot
        markers[gray > 150] = 1  # seen as black in plot

        # Segment with watershed using elevation map
        segmentation = morphology.watershed(elevation_map, markers)
        segmentation = ndi.binary_fill_holes(segmentation - 1)
        # labeled_image, n = ndi.label(segmentation)

        # Watershed with distance transform
        kernel = numpy.ones((5, 5), numpy.uint8)

        distance = ndi.distance_transform_edt(segmentation)
        distance2 = cv2.erode(distance, kernel)
        distance2 = cv2.dilate(distance2, kernel)
        local_max = peak_local_max(distance2, num_peaks=1, indices=False, labels=segmentation)
        markers2 = ndi.label(local_max)[0]
        labels = morphology.watershed(-distance2, markers2, mask=segmentation)

        # Extract regions (caching signifies more memory use)
        regions = regionprops(labels, cache=True)

        # Filter out big wrong regions
        regions = [region for region in regions if region.area < 1000]

        # Set count
        analysis.count = len(regions)

        # Set name
        analysis.name = 'Red cell count'

        return analysis
