import cv2
import numpy
from scipy import ndimage as ndi
from skimage import morphology
from skimage import exposure
from skimage.feature import peak_local_max
from skimage.measure import regionprops

from project.analysis.type.base import AnalysisType
from project.util.image_utils import ImageUtils

try:
    import skimage.filters as filters
except:
    import skimage.filter as filters


class RedCellCount(AnalysisType):
    name = 'BLOOD_RED-CELL-COUNT'
    image_utils = ImageUtils()

    def analyse(self, **kwargs):
        image_object = kwargs['image']

        if image_object is None:
            raise RuntimeError()

        # Read the image
        image = cv2.imread(self.image_utils.getOutputFilename(image_object.id))

        if image is None:
            print('File not found')
            return

        # Work on green channel
        gray = image[:, :, 1]

        # Apply otsu thresholding
        thresh = filters.threshold_otsu(gray)
        gray[gray < thresh] = 0

        # Apply histogram equalization
        gray = exposure.equalize_adapthist(gray) * 255

        # Create elevation map
        elevation_map = filters.sobel(gray)

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

        # Set result
        result = str(len(regions))

        return result
