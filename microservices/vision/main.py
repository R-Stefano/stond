from plantcv import plantcv as pcv
import numpy as np
import cv2

def displayImage(array):
    #print(array)
    cv2.imshow("image", array)
    cv2.waitKey()
    cv2.destroyWindow("image")

imagePath = "./test_data/test1.jpeg"
outputDir = "./test_data/output/"

img, path, filename = pcv.readimage(imagePath)
img = img[:, 100:-200]

colorspace_img = pcv.visualize.colorspaces(rgb_img=img)
pcv.print_image(colorspace_img, outputDir + 'colorspace.png')

# Convert RGB to HSV and extract the saturation channel
s = pcv.rgb2gray_hsv(img, 's')

# Threshold the saturation image
# TODO: This step is often one that needs to be adjusted depending on the lighting and configurations of your camera system.
thresholdValue = 170 # Value from which the image is set to whi
s_thresh = pcv.threshold.binary(s, thresholdValue, 255, 'light')

# Median Blur
s_mblur = pcv.median_blur(s_thresh, 5)
s_cnt = pcv.median_blur(s_thresh, 5)

# Convert RGB to LAB and extract the Blue channel
b = pcv.rgb2gray_lab(img, 'b')

# Threshold the blue image
b_thresh = pcv.threshold.binary(b, 160, 255, 'light')
b_cnt = pcv.threshold.binary(b, 160, 255, 'light')

# Join the thresholded saturation and blue-yellow images
bs = pcv.logical_or(s_mblur, b_cnt)

# Apply Mask (for VIS images, mask_color=white)
masked = pcv.apply_mask(img, s_thresh, 'white')

# Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
masked_a = pcv.rgb2gray_lab(masked, 'a')
masked_b = pcv.rgb2gray_lab(masked, 'b')

# Threshold the green-magenta and blue images
maskeda_thresh = pcv.threshold.binary(masked_a, 115, 255, 'dark')
maskeda_thresh1 = pcv.threshold.binary(masked_a, 135, 255, 'light')
maskedb_thresh = pcv.threshold.binary(masked_b, 128, 255, 'light')


# Join the thresholded saturation and blue-yellow images (OR)
ab1 = pcv.logical_or(maskeda_thresh, maskedb_thresh)
ab = pcv.logical_or(maskeda_thresh1, ab1)

# Fill small objects
ab_fill = pcv.fill(ab, 200)
# Apply mask (for VIS images, mask_color=white)
masked2 = pcv.apply_mask(masked, ab_fill, 'white')

pcv.print_image(masked2, outputDir + 'white_mask.png')

# Identify objects
id_objects, obj_hierarchy = pcv.find_objects(masked2, ab_fill)

 # Define ROI
roi1, roi_hierarchy= pcv.roi.rectangle(x=200, y=100, h=800, w=700, img=masked2)

# Decide which objects to keep
roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img, roi_type='partial', roi_contour=roi1, roi_hierarchy=roi_hierarchy, object_contour=id_objects, obj_hierarchy=obj_hierarchy)

pcv.params.debug = "print"
pcv.params.debug_outdir = outputDir
pcv.params.device = 1

# Object combine kept objects
obj, mask = pcv.object_composition(img, roi_objects, hierarchy3)

pcv.print_image(mask, outputDir + 'mask.png')

# Find shape properties, output shape image (optional)
shape_image = pcv.analyze_object(img, obj, mask)
plant_solidity = pcv.outputs.observations['default']['solidity']
plant_area = pcv.outputs.observations['default']['area']
plant_height = pcv.outputs.observations['default']['height']
plant_width = pcv.outputs.observations['default']['width']
plant_center_of_mass = pcv.outputs.observations['default']['center_of_mass']

#Using 100 dpi
analytics = {
    "height": 	0.0254 * plant_height['value'],
    "width": 	0.0254 * plant_width['value'],
    "area": 	0.0254 * plant_area['value'],
}

print(analytics)

'''

# Shape properties relative to user boundary line (optional)
boundary_image = pcv.analyze_bound_horizontal(img, obj, mask, 1680)
displayImage(boundary_image)

# Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
histogram_image = pcv.analyze_color(img, kept_mask)
displayImage(histogram_image)




background subtraction 
green-magent - blue-yellow channels (obtaining from lab color space instead or rgb) experimenting with different color spaces 
to determine where the best the plant pops up compared to background resulted in hsv and lab colors spaces  


'''


