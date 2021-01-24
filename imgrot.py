import cv2
import numpy as np
import os
import read_tps
import sys

def normalize(x):
  return (1 / np.linalg.norm(x)) * x

def affmul(A, B):
  Bmod = np.concatenate((B, np.array([[0, 0, 1]])), axis=0)
  return np.matmul(A, Bmod)

def affapply(A, x):
  xmod = np.concatenate((x, np.ones(1)), axis=0)
  return np.matmul(A, xmod)

if __name__ == '__main__':
  tps_file = sys.argv[1]
  tps_dir = os.path.dirname(tps_file)
  output_dir = os.path.join(tps_dir, 'imgrot')
  for entry in read_tps.read_tps(tps_file):
    print('processing image "{}"'.format(entry['image']))
    lms = entry['landmarks']
    if len(lms) < 2:
      print('- less than 2 landmarks, skipping')
      continue 

    top = np.array(lms[0])
    bot = np.array(lms[1])
    mid = 0.5 * (top + bot)
    T0 = np.array([[1, 0, -mid[0]], [0, 1, -mid[1]]])
    dir_y = normalize(bot - top)
    dir_x = np.array([dir_y[1], -dir_y[0]])
    R = np.array([[dir_x[0], dir_x[1], 0], [dir_y[0], dir_y[1], 0]])
    A0 = affmul(R, T0)

    img_file = os.path.join(tps_dir, entry['image'])
    img = cv2.imread(img_file)

    mins = np.zeros((2))
    maxes = np.zeros((2))
    corners = [np.array((x,y)) for x in [0, img.shape[1]] for y in [0, img.shape[0]]]
    for corner in corners:
      tf_corner = affapply(A0, corner)
      mins = np.minimum(mins, tf_corner)
      maxes = np.maximum(maxes, tf_corner)
    T1 = np.array([[1, 0, -mins[0]], [0, 1, -mins[1]]])
    A1 = affmul(T1, A0)
    diff = maxes - mins
    dims = (int(diff[0] + 0.5), int(diff[1] + 0.5))

    if not os.path.isdir(output_dir):
      os.makedirs(output_dir)
    out_file = os.path.join(output_dir, entry['image'])
    cv2.imwrite(out_file, cv2.warpAffine(img, A1, dims))
