import json
import numpy as np
from pycocotools import mask
from skimage import measure
import cv2

#Find convex hull and draw convex hull with maximum area. This helps to remove the small noisy areas in the image
import matplotlib.pyplot as plt
def find_hull(prediction):  # Input the segmented image from the model. Function outputs the convex hull with maximum area.
    prediction = prediction.astype(np.uint8) 
    contours, hierarchy = cv2.findContours(prediction, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find contours using opencv
    if len(contours)!=0:
        hull = []
        for i in range(len(contours)): # Find convex hull for each contour set
            hull.append(cv2.convexHull(contours[i], False))
        drawing = np.zeros((prediction.shape[0], prediction.shape[1], 3)) # Create an empty black image
        color = (255, 255, 255) # hull color
        c = max(hull, key = cv2.contourArea) # Find hull with maximum area
        m = []
        m.append(c)
        return m

for i in range(0,147):
    hull = []
    path = '/Users/sonudileep/Downloads/Mask_606/' + str(i) + '.png' 
    ground_truth_binary_mask = cv2.imread(path,0)
    ground_truth_binary_mask = ground_truth_binary_mask/255
    ground_truth_binary_mask = ground_truth_binary_mask.astype(np.uint8)
    countzero_in1 = not np.any(ground_truth_binary_mask)
    #print(i, countzero_in1)
    if countzero_in1==True:
        continue    
    hull = find_hull(ground_truth_binary_mask)
    #print(hull)
    fortran_ground_truth_binary_mask = np.asfortranarray(ground_truth_binary_mask)
    encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
    ground_truth_area = mask.area(encoded_ground_truth)
    ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
    contours = measure.find_contours(ground_truth_binary_mask, 0.5)
    null = 'null'
    annotation = {
            "version": "4.5.6",
            "flags": {},
            "shapes": [{ "label" : "1",
                        "points" : " ",
                        "group_id": null,
                        "shape_type": "polygon",
                        "flags": {} 
                        }],
            "imagePath": ""       
        }
    yy = 0
#     for contour in contours:
#         contour = np.flip(contour, axis=1)
#         segmentation = contour.ravel().tolist()
#         print(type(segmentation))
    temp = []
    points = []
    #print(hull[0].shape[0])
    for k in range(hull[0].shape[0]):
#        print(hull[0][k][0][0], hull[0][k][0][1])
        points.append([float(hull[0][k][0][0]), float(hull[0][k][0][1])])
  #      points.append(hull[0][k][0])
   # print(points)
    annotation["shapes"][0]["points"] = points
    annotation["imagePath"]= str(i) + ".jpg"
#    print(annotation)
    path_1 = '/Users/sonudileep/Downloads/Mask_606/' + str(i) + '.json'
    m = json.dumps(annotation, indent=4)
    json_path = "/Users/sonudileep/Downloads/Image_606/" + str(i) + ".json"
    text_file = open(json_path, "w")
    n = text_file.write(m)
    text_file.close()
