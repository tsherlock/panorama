Project 1: Panorama stitching
========

## Due: 23 Sept 2014, 11:59pm

<a href="http://en.wikipedia.org/wiki/File:SonyCenter_360panorama.jpg"><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/6/65/SonyCenter_360panorama.jpg/1024px-SonyCenter_360panorama.jpg"/></a>

In this project, you'll write software that stitches multiple images of a scene together into a panorama automatically. A panorama is a composite image that has a wider field of view than a single image, and can combine images taken at different times for interesting effects.

Your image stitcher will, at a minimum, do the following:
* locate corresponding points between a pair of images
* use the corresponding points to fit a homography (2D projective transform) that maps one image into the space of the other
* use the homography to warp images into a common target frame, resizing and cropping as necessary
* composite several images in a common frame into a panorama

While I encourage you to make use of OpenCV's powerful libraries, for this project you must not use any of the functions in the [`stitcher`](http://docs.opencv.org/modules/stitching/doc/stitching.html) package (although you're welcome to read its documentation and code for inspiration).

### Find a homography between two images (40 points + up to 20 bonus points)

A [homography](http://en.wikipedia.org/wiki/Homography_(computer_vision)) is a 2D projective transformation, represented by a 3x3 matrix, that maps points in one image frame to another, assuming both images are captured with an ideal pinhole camera.

#### Feature matching

To establish a homography between two images, you'll first need to find a set of correspondences between them. One common way of doing this is to identify "interest points" or "key points" in both images, summarize their appearances using descriptors, and then establish matches between these "features" (interest points combined with their descriptors)  by choosing features with similar descriptors from each image.

You're welcome to establish correspondences any way you like. I would recommend you consider extracting keypoints and descriptors using the [cv2.SIFT](http://docs.opencv.org/modules/nonfree/doc/feature_detection.html#sift) interface to compute interest points and descriptors, and using one of [the descriptor matchers OpenCV provides](http://docs.opencv.org/modules/features2d/doc/common_interfaces_of_descriptor_matchers.html) under a common interface.

You'll probably find it useful to visualize the matched features between two images to see how many of them look correct. It's a good bet that you'll have some incorrect matches, or "outliers". You can experiment with different feature extraction and matching techniques to try to reduce the number of outliers. The fewer there are, the better the fit of your homography will be, although you'll never be able to eliminate all of them.

#### Fitting the homography

Once you've established correspondences between two images, you'll use them to find a "best" homography mapping one image into the frame of another. Again, you're welcome to do this any way you like, but I suggest you consider looking at [cv2.findHomography](http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#findhomography), which can compute the least-squares-best-fit homography given a set of corresponding points. It also offers robustified computation using RANSAC or the Least-Median methods. You'll likely need to tweak the robustifiers' parameters to get the best results.

#### Evaluating success

The unit tests include `test_homography`, which will evaluate the difference between your computed homography and a "ground truth" known homography. If your homography is close enough to ground truth for this test to pass, you'll receive full credit. You'll lose points as the accuracy of your homography declines.

#### Bonus credit

I will evaluate your homography computation with a broad selection of input images and ground-truth homographies, and measure the distribution of error norms. The most accurate implementation in class will recieve 20 bonus points. The second most accurate will receive 16, the third 12, the fourth 8, and the fifth 4.

I expect you'll need to delve into the details of feature matching and robust fitting to achieve the highest possible accuracy.

### Image warping (20 points)

Once you've found homographies mapping all images into a common frame, you'll need to actually warp them according to these homographys before you can composite them together. This process is also referred to as "image rectification." A good place to start is [cv.warpPerspective](http://docs.opencv.org/modules/imgproc/doc/geometric_transformations.html#void warpPerspective(InputArray src, OutputArray dst, InputArray M, Size dsize, int flags, int borderMode, const Scalar& borderValue)), but be aware that out-of-the-box, it may map images outside the target image coordinates.

In addition to warping the image, you should add an alpha channel so that pixels not covered by the warped input image are "clear" before compositing. For a full specification of the expected behavior, see the function comment for `warp_image()` and its corresponding unit tests.

### Image mosaicing (20 points)

Composite your images together into a mosaic to form the final output panorama. You don't need to blend the images together (although you can for extra credit; see below), but there should be no occlusion of one image by another except where at least one image has valid warped pixels.

### Write up and results (20 points)

Capture at least one set of three or more images using any camera you like (your phone's camera will probably do fine) and stitch the images together into a panorama with your implementation. Add the source images, the panorama, and a script that can regenerate the pano from your implementation into the `my_panos` folder.

If you want, play around! Try taking a panorama where the same person or object appears multiple times. Try distant and close up scenes to see the effects of parallax on your solution. Place any interesting panos in the `my_panos` folder and I'll share the results with the class.

### Extra credit (maximum of 50 points)

There's a lot more to explore in the world of homographies and panorama stitching. Implement as many of the below as you like for extra credit. Be sure to include code for the extra credit as part of your check-in. Also, please add a PDF write-up describing which extra credit you implemented called `extra_credit.pdf` in the project_1 directory so we can see your results.

#### 10 points: Panorama of a planar scene

Instead of taking all of your panoramas from the same spot, create a panorama by moving linearly along in front of a planar scene. Report your results and the challenges of taking such a pano.

#### 10 points: Image cut-out compositing

Identify a known planar surface in an image and composite a planar image onto it. You can use this technique to add graffiti or a picture of your self to an image of a building.

#### 10-20 points: Blending

Implement some form of alpha blending between overlapping images. Some possibilities include feathering, pyramid blending, or multi-band blending. The more sophisticated and higher-quality blending you use, the more points you'll earn.

<img src="http://docs.opencv.org/trunk/_images/orapple.jpg" />

#### 20 points: Spherical stitching

Instead of mapping all of your images into a single perspective frame, map them into spherical coordinates (this will require a guess of the focal length of the camera). This will allow you to create any spherical projection of your panorama, like the lovely "little planet":

<a href="http://commons.wikimedia.org/wiki/File:Globe_panorama03.jpg#mediaviewer/File:Globe_panorama03.jpg"><img width="800" src="http://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Globe_panorama03.jpg/1200px-Globe_panorama03.jpg" alt="Globe panorama03.jpg"></a>

Or the equirectangular projection:

<a href="http://en.wikipedia.org/wiki/File:SonyCenter_360panorama.jpg"><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/6/65/SonyCenter_360panorama.jpg/1024px-SonyCenter_360panorama.jpg"/></a>

Such panos will look better if they cover as much of the sphere as possible.

## Logistics

You will work on this project in randomly assigned groups of three. All group members should have identical submissions in each of their private repositories by the project due date. We will select one group member's repository, clone it, and use it to compute the grade for all group members.

If the group chooses to turn in a project N days late, each individual in the group will lose N of their remaining late days for the semester. If one or more students have no more late days left, they'll lose credit without affecting the other group members' grades.


