import cv2
import pano_stitcher
import numpy

left = cv2.imread("3.jpg",-1)
right = cv2.imread("5.jpg",-1)
right2 = cv2.imread("6.jpg",-1)
middle = cv2.imread("4.jpg",-1)
left1 = cv2.imread("2.jpg",-1)
left2 = cv2.imread("1.jpg",-1)

leftImages = [left2, left1, left]
rightImages = [right2, right]

while len(leftImages) > 1:
	print "Left Image Loop"
	image = leftImages.pop(0)
	homo = pano_stitcher.homography(leftImages[0], image)
	warped, origin = pano_stitcher.warp_image(image, homo)
	leftImages[0] = pano_stitcher.create_mosaic([warped, cv2.cvtColor(leftImages[0],cv2.COLOR_BGR2BGRA)], [origin, (0,0)])
	leftImages[0] = cv2.cvtColor(leftImages[0],cv2.COLOR_BGRA2BGR)

left_pano = leftImages[0]
cv2.imshow("sup", left_pano)
cv2.waitKey()

while len(rightImages) > 1:
	print "Right Image Loop"
	image = rightImages.pop(0)
	homo = pano_stitcher.homography(rightImages[0], image)
	warped, origin = pano_stitcher.warp_image(image, homo)
	rightImages[0] = pano_stitcher.create_mosaic([warped, cv2.cvtColor(rightImages[0],cv2.COLOR_BGR2BGRA)], [origin, (0,0)])
	leftImages[0] = cv2.cvtColor(leftImages[0],cv2.COLOR_BGRA2BGR)

right_pano = rightImages[0]

print "Finished left and right panos"

print "Doing left pano homography and warp"
leftHomo = pano_stitcher.homography(middle, left_pano)
warpedLeft, leftOrigin = pano_stitcher.warp_image(left_pano, leftHomo)

print "Doing right pano homography and warp"
rightHomo = pano_stitcher.homography(middle, right_pano)
warpedRight, rightOrigin = pano_stitcher.warp_image(right_pano, rightHomo)

print "Finished warps"

middle = cv2.cvtColor(middle, cv2.COLOR_BGR2BGRA)

images = [warpedRight, warpedLeft, middle]
origins = [rightOrigin,leftOrigin, (0, 0)]

pano = pano_stitcher.create_mosaic(images, origins)
print "Attempting final pano stitch"
cv2.imwrite('mypanos.png', pano)
