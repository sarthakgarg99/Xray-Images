import numpy as np
import cv2
import imageio
import numpy as np
from scipy.ndimage.filters import gaussian_filter, median_filter, maximum_filter, minimum_filter
from skimage import img_as_float
import os
import timeit



# Give appropriate input image and output image location

image_file = 'Images/TopCar6-gray-log.jpg'
output_file = 'output/TopCar6-gray-log-UM.jpg'


class UM():
    def __init__(self, filename, radius, amount):
        self.filename = filename
        self.radius = radius
        self.amount = amount

    def run(self):

        image = imageio.imread(self.filename)
        image = img_as_float(image) # ensuring float values for computations

        blurred_image = gaussian_filter(image, sigma=self.radius)

        mask = image - blurred_image # keep the edges created by the filter
        
        sharpened_image = image + mask * self.amount

        sharpened_image = np.clip(sharpened_image, float(25/255), float(1)) # Interval [0.0, 1.0]
        sharpened_image = (sharpened_image*255).astype(np.uint8) # Interval [0,255]

        mask_image = mask * self.amount
        mask_image = np.clip(mask_image, float(0), float(1)) # Interval [0.0, 1.0]
        mask_image = (mask_image*255).astype(np.uint8) # Interval [0,255]               

        return sharpened_image



 # Maximum slider
MAX_VALUE = 30
MAX_VALUE2 = 30
 # Slider minimum
MIN_VALUE = 0
 
 # Adjust the saturation and brightness window
cv2.namedWindow("radius and amount", cv2.WINDOW_GUI_NORMAL)
 
 # Create sliding block
cv2.createTrackbar("radius", "radius and amount",
                    MIN_VALUE, MAX_VALUE, lambda x:x)
cv2.createTrackbar("amount", "radius and amount",
                    MIN_VALUE, MAX_VALUE2, lambda x:x)
 
while True:

    radius = cv2.getTrackbarPos('radius', 'radius and amount')
    amount = cv2.getTrackbarPos('amount', 'radius and amount')

    model = UM(image_file, int(radius), int(amount))
    lsImg = model.run()    
    lsImg = cv2.applyColorMap(lsImg, cv2.COLORMAP_BONE)
    
    cv2.imshow("radius and amount", lsImg)
    ch = cv2.waitKey(5)
         # Press ESC to exit
    if ch == 27:
        break
    elif ch == ord('s'):
                 # Press s to save and exit
        print('Saving and exiting')
        cv2.imwrite(output_file, lsImg)
        break
    
print("radius:",int(radius))
print("amount:",int(amount))
 # Close all windows
cv2.destroyAllWindows()