'''
import ssd_utils
import pickle
import numpy as np


# p.shape = (7308, 8)
# p[i] = [xmin, ymin, xmax, ymax, varxc, varyc, varw, varh].
# Always (varxc, varyc, varw, varh) = (0.1, 0.1, 0.2, 0.2)
p = pickle.load(open('prior_boxes_ssd300.pkl', 'rb'))
# gt[key].shape = (x, 7)
# x means box number
# 7 means classes_number + 4, classes number not include background number
# (+4) means dxmin, dymin, dxmax, dymax
# So gt = [dxmin, dymin, dxmax, dymax, (classes one-hot array)]
gt = pickle.load(open('gt_pascal.pkl', 'rb'))
y = gt['frame04467.png'].copy()
# Class number = 4, include background class
bb = ssd_utils.BBoxUtility(4, p)
# yy.shape = (7308, 16)
yy = bb.assign_boxes(y)

targets = []
targets.append(yy)
tmp_targets = np.array(targets)
results = bb.detection_out(tmp_targets)

# Input is img_resize, Output is bbox.assign_boxes(gt[key])
'''

'''
import main_fit
#voc = main_fit.VOC_Tool('../../Train/VOC2012', ['cat', 'car', 'dog', 'person'], (300, 300, 3))
voc = main_fit.VOC_Tool('../../Train/VOC2012', ['car'], (300, 300, 3))
#voc.loadCheckpoint('save.h5')
voc.initModel()
voc.fit(1024, 'car')
'''

from main_fit import VOC_Tool
import cv2
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from keras.preprocessing import image as imp
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # or any {'0', '2', '3'}
image = []

x_tmp = cv2.imread('image/2008_002197.jpg')
#x_tmp = cv2.resize(x_tmp, (300, 300))
x_tmp = x_tmp[...,::-1]
x_tmp = x_tmp.astype(np.float32)

img = imp.load_img('image/2008_002197.jpg', (300, 300))
img = imp.img_to_array(img)
#img = np.array(img)
image.append(img)
voc = VOC_Tool('../../Train/VOC2012', ['car'], (300, 300, 3))
voc.loadCheckpoint('save.h5')
voc.initModel()
(img, ans) = voc.predict('image/2008_002197.jpg')
gt = voc.getAssignBoxes('2008_002197', 'car')
# <Debug>
# This is not very influential for the answer
#(x_tmp, gt) = voc.random_sized_crop(x_tmp, gt)
# </Debug>
# <TODO id=190809000>
# <Comment>
#     It's return shape(num_boxes, 4 + num_classes + 8), and is array([0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
# </Comment>
# <Comment>
#     voc.bbox.encode_box() return shape(-1, -1, 4(location_inf) + 1(IoU))
#     encoded_boxes.shape = (1, 7308, 5)
#     encode_boxes some answer:
#     [ 1.65789473  2.20878693  1.43182712 -0.06122396  0.50121087]
#     [ 1.36569814  1.81949905  0.46241309 -1.03063696  0.53675264]
#     [ 0.40503537  3.8257325  -0.67460308  2.68530666  0.51681804]
#     [-0.97368476  2.20878693  1.43182673 -0.06122396  0.50121086]
#     [-0.80207666  1.81949905  0.46241373 -1.03063696  0.58948563]
#     [-0.6884986   3.12369748 -0.30104073  1.67164387  0.52714906]
#     [ 1.65789473 -0.4227909   1.43182712 -0.06122357  0.69781443]
#     [ 1.36569814 -0.34827588  0.46241309 -1.03063761  0.64492539]
#     [ 1.03430957 -0.59791663 -0.12395084  1.67164442  0.59813611]
#     [ 0.40503537 -0.7322953  -0.67460308  2.685307    0.5389622 ]
#     [-0.97368476 -0.4227909   1.43182673 -0.06122357  0.69781452]
#     [-0.80207666 -0.34827588  0.46241373 -1.03063761  0.7132179 ]
#     [-0.6884986  -0.59791663 -0.30104073  1.67164442  0.63811338]
#     [-0.80207666 -2.51605121  0.46241373 -1.03063761  0.50427992]
#     [ 0.23214317  2.39167767 -0.50700059 -2.00005128  0.50462895]
#     [ 1.31074104 -1.66842012  0.10000749 -0.26718326  0.56416066]
#     [ 0.35066305 -2.0433891  -0.72515561  0.74647979  0.60806138]
#     [ 0.23214317 -1.17975128 -0.50700059 -2.00005075  0.60567587]
#     [-0.50274286 -1.66842012 -1.59391963 -0.26718326  0.5323169 ]
#     [-0.4632794  -1.26258812 -1.55023597 -1.66075057  0.52613503]
#
#     best_iou = encoded_boxes[:, :, -1].max(axis=0) get IoU Array(axis=0)
#     best_iou: array([0, 0, ..., 0.50121087, ..., 0.53675264, ..., 0])
# </Comment>
# </TODO>

voc.showPredictImg(image[0], gt)
#voc.showPredictImg(image[0], ans)
