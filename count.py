#
# python 3 script to count things (birds) in images
#
# initially based on https://stackoverflow.com/questions/48154642/how-to-count-number-of-dots-in-an-image-using-python-and-opencv
#
# to use:
# 1. make a duplicate small crop of the jpg that contains dots/birds in most of the
#      range from small to large that are visible in the image.
# 2. change the area_lower_bound and area_upper_bound variables below.
# 3. run the script, providing a path to the cropped image, and ensure it outputs
#      an image with just about all the spots highlighted with no spurious tiny
#      spots highlighted.  adjust the bounds variables and try again as needed.
# 4. run the script with the full, uncropped image
#
# tips:
# - it may be helpful to use photoshop or similar to paint over high-contrast areas
#     with a solid color where those areas should not be counted
# - for noisy images using strong de-noising or gentle blurring, that still allows
#     the spots to be seen and counted, will significantly speed up the processing time
#

import cv2
import random
import sys
import time

from pathlib import Path

def get_path_with_new_filename_prefix(pathstr, new_prefix):
	p = Path(pathstr)
	p_name = p.name
	p = p.with_name(f'{new_prefix}{p_name}')
	return str(p)

img_path = sys.argv[1]

print(f'reading file...')
img_color = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

print(f'thresholding...')
#th, threshed = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
threshed = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

print(f'finding contours...')
contours = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
print(f'found {len(contours)} potential spots')

#######################
# C H A N G E
# lower and upper bounds below, for spot area
# (can watch output, and if finding way too many spots terminate and adjust)
#######################
area_lower_bound = 200
area_upper_bound = 2000
pct_done = 0.0
found = 0

for i in range(len(contours)):
	if i % 1_000 == 0:
		print(f'{round((float(i)*100.0)/float(len(contours)),2)}%: checking countour {(i+1)}')
	if area_lower_bound <= cv2.contourArea(contours[i]) <= area_upper_bound:
		found += 1
		if found % 100 == 0:
			print(f'found {found} spots with desired area')
		# pick a random color so neighboring spots can be visually distinguished
		#spot_contour_color = random.sample([(205,250,45),(255,150,45),(245,75,211),(100,150,255),(160,60,255)], 1)[0]
		spot_contour_color = random.sample([(0,220,220),(120,255,255),(220,220,0),(255,255,120),(220,0,220),(255,120,255),(255,120,120),(120,255,120),(120,120,255),(255,220,220),(220,255,220),(220,220,255)], 1)[0]
		cv2.drawContours(img_color, contours, i, spot_contour_color, 2, cv2.LINE_8)

prefixed_path = get_path_with_new_filename_prefix(img_path, f'spots-{area_lower_bound}-to-{area_upper_bound}-found-{found}-{int(time.time())}-')
print(f'writing file [{prefixed_path}]');
cv2.imwrite(prefixed_path, img_color)

print(f"found [{found}] spots")
