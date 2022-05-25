import sim
import time
import numpy as np
# import math

from PIL import Image as I
import array

import cv2, numpy

# def track_green_object(image):

#     # Blur the image to reduce noise
#     blur = cv2.GaussianBlur(image, (5,5),0)

#     # Convert BGR to HSV
#     hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

#     # Threshold the HSV image for only green colors
#     lower_green = numpy.array([40,70,70])
#     upper_green = numpy.array([80,200,200])

#     # Threshold the HSV image to get only green colors
#     mask = cv2.inRange(hsv, lower_green, upper_green)
    
#     # Blur the mask
#     bmask = cv2.GaussianBlur(mask, (5,5),0)

#     # Take the moments to get the centroid
#     moments = cv2.moments(bmask)
#     # moments = cv2.moments(mask)
#     m00 = moments['m00']
#     centroid_x, centroid_y = None, None
#     if m00 != 0:
#         centroid_x = int(moments['m10']/m00)
#         centroid_y = int(moments['m01']/m00)

#     # Assume no centroid
#     ctr = None

#     # Use centroid if it exists
#     if centroid_x != None and centroid_y != None:
#         ctr = (centroid_x, centroid_y)
#     return ctr

# def contur(image):

# #!!! Выделяются линии !!!
#   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#   edges = cv2.Canny(gray, 50, 200)

# # Detect points that form a line

#   linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=10, maxLineGap=250)
  
#   if linesP is not None:
#       for i in range(0, len(linesP)):
#           l = linesP[i][0]
#           cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

#   #!!! Выделяются углы !!!

#   operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#   # изменить тип данных
#   # установка 32-битной плавающей запятой
#   operatedImage = np.float32(operatedImage)

#   # применить метод cv2.cornerHarris
#   # для определения углов с соответствующими
#   # значения в качестве входных параметров
#   dest = cv2.cornerHarris(operatedImage, 2, 3, 0.04)

#   # Результаты отмечены через расширенные углы
#   dest = cv2.dilate(dest, None)

#   # # Возвращаясь к исходному изображению,
#   # # с оптимальным пороговым значением
#   image[dest > 0.05 * dest.max()] = [255, 255, 255]

#   #!!! Выделяется контур !!!
    
#   grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#   ret, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)

#   contours, hierarchy = cv2.findContours(binImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#   img_contours = np.zeros(image.shape)

#   cv2.drawContours(image, contours, -1, (255, 255, 255), 1)

#     #!!! Др контур !!!

#   hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     ## 1
#   green_low = np.array([45, 100, 50] )
#   green_high = np.array([75, 255, 255])
#   curr_mask = cv2.inRange(hsv_img, green_low, green_high)
#   hsv_img[curr_mask > 0] = ([75,255,200])
#   # 2
#   # converting the HSV image to Gray inorder to be able to apply 
#   # contouring
#   RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
#   gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)
#   # 3
#   ret, threshold = cv2.threshold(gray, 90, 255, 0)
#   # 4
#   contours, hierarchy =  cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#   cv2.drawContours(image, contours, -1, (255, 255, 255), 1)

def save_image(image):
    # путь к указанному входному изображению и
  # изображение загружается с помощью команды imread
  # image = cv2.imread('DSCN1311.jpg')

  # конвертировать входное изображение в Цветовое пространство в оттенках серого
  operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # изменить тип данных
  # установка 32-битной плавающей запятой
  operatedImage = np.float32(operatedImage)

  # применить метод cv2.cornerHarris
  # для определения углов с соответствующими
  # значения в качестве входных параметров
  dest = cv2.cornerHarris(operatedImage, 2, 5, 0.07)

  # Результаты отмечены через расширенные углы
  dest = cv2.dilate(dest, None)

  # Возвращаясь к исходному изображению,
  # с оптимальным пороговым значением
  
  image[dest > 0.05 * dest.max()] = [0, 0, 255]
  # окно с выводимым изображением с углами
  

  if cv2.waitKey(0) & 0xff == 27:
      cv2.destroyAllWindows()

sim.simxFinish(-1)

clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
  print('Connected to remote API server')

  # get vision sensor objects
  res, v0 = sim.simxGetObjectHandle(clientID, 'v0', sim.simx_opmode_oneshot_wait)
  res, v1 = sim.simxGetObjectHandle(clientID, 'v1', sim.simx_opmode_oneshot_wait)
  res, v2 = sim.simxGetObjectHandle(clientID, 'v2', sim.simx_opmode_oneshot_wait)

  err, resolution, image = sim.simxGetVisionSensorImage(clientID, v0, 0, sim.simx_opmode_streaming)
  time.sleep(1)
  flage = True
  while (sim.simxGetConnectionId(clientID) != -1):
    # get image from vision sensor 'v0'
    err, resolution, image = sim.simxGetVisionSensorImage(clientID, v0, 0, sim.simx_opmode_buffer)
    
    if err == sim.simx_return_ok:
      image_byte_array = array.array('b', image)
      # !!!!!Ошибка тут!!!!
      br=bytes(image_byte_array)
      image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), br, "raw", "RGB", 0, 1)

      img2 = numpy.asarray(image_buffer)

      img3 = numpy.array(image_buffer)
      save_image(img3)
      #con = contur(img3)

      # try to find something green
      #ret = track_green_object(img2)

      # overlay rectangle marker if something is found by OpenCV
      #if ret:
      #  cv2.rectangle(img2,(ret[0]-15,ret[1]-15), (ret[0]+15,ret[1]+15), (0xff,0xf4,0x0d), 1)


      # return image to sensor 'v1'
      img2 = img2.ravel()
      sim.simxSetVisionSensorImage(clientID, v1, img2, 0, sim.simx_opmode_oneshot)

      img3 = img3.ravel()
      sim.simxSetVisionSensorImage(clientID, v2, img3, 0, sim.simx_opmode_oneshot)
    
    elif err == sim.simx_return_novalue_flag:
      print("no image yet")
      pass
    else:
      print(err)
else:
  print("Failed to connect to remote API Server")
  sim.simxFinish(clientID)