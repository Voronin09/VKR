from PIL import Image as I
import sim
import time
import array
import numpy
import cv2

def search_green(pic):

    # Уменьшаем шум, используя размытие
    pic1 = cv2.GaussianBlur(pic, (5,5),0)

    #преобразование форматов изображения из RGB в HSV
    hsv = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)

    # Порог для целеных цветов
    lower_green = numpy.array([40,70,70])
    upper_green = numpy.array([80,200,200])

  
    #оставляtv значения в пределах заданных цвета
    pic2 = cv2.inRange(hsv, lower_green, upper_green)
    
    # Уменьшаем шум, используя размытие
    pic3 = cv2.GaussianBlur(pic2, (5,5),0)

    #  Воспользуйтесь моментом, чтобы получить   центроид
    pic4 = cv2.moments(pic3)
    # Момент нулевого порядка, т.е. кол-во всех точек маски
    zero_moment = pic4['m00']
    # готовим координаты центроида
    x, y = None, None
    #Если найдены зеленые точки, то мы ищем центр фигуры зеленых, состоящей из зеленых точек
    if zero_moment != 0:
        x = int(pic4['m10']/zero_moment)#сумма Х координат точек/на кол-во точек
        y = int(pic4['m01']/zero_moment)#сумма Y координат точек/на кол-во точек

    # Предположим, что нет центроида
    coords = None

    # если функция нашла центроид, то возвращаем его координаты
    if x != None and y != None:
        coords = (x, y)
    return coords

def search_blue(pic):

    # Уменьшаем шум, используя размытие
    pic1 = cv2.GaussianBlur(pic, (5,5),0)

    #преобразование форматов
    hsv = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)

    # Порог для целеных цветов
    lower_blue = numpy.array([0,70,70])
    upper_blue = numpy.array([39,200,200])

  
    #оставляtv значения в пределах заданных цвета
    pic2 = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Уменьшаем шум, используя размытие
    pic3 = cv2.GaussianBlur(pic2, (5,5),0)

    #  Воспользуйтесь моментом, чтобы получить   центроид
    pic4 = cv2.moments(pic3)
    # Момент нулевого порядка, т.е. кол-во всех точек маски
    zero_moment = pic4['m00']
    # готовим координаты центроида
    x, y = None, None
    #Если найдены зеленые точки, то мы ищем центр фигуры зеленых, состоящей из зеленых точек
    if zero_moment != 0:
        x = int(pic4['m10']/zero_moment)#сумма Х координат точек/на кол-во точек
        y = int(pic4['m01']/zero_moment)#сумма Y координат точек/на кол-во точек

    # Предположим, что нет центроида
    coords = None

    # если функция нашла центроид, то возвращаем его координаты
    if x != None and y != None:
        coords = (x, y)
    return coords

def search_red(pic):

    # Уменьшаем шум, используя размытие
    pic1 = cv2.GaussianBlur(pic, (5,5),0)

    #преобразование форматов
    hsv = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)

    # Порог для целеных цветов
    lower_red = numpy.array([81,70,70])
    upper_red = numpy.array([255,200,200])
    #оставляtv значения в пределах заданных цвета
    pic2 = cv2.inRange(hsv, lower_red, upper_red)
    
    # Уменьшаем шум, используя размытие
    pic3 = cv2.GaussianBlur(pic2, (5,5),0)

    #  Воспользуйтесь моментом, чтобы получить   центроид
    pic4 = cv2.moments(pic3)
    # Момент нулевого порядка, т.е. кол-во всех точек маски
    zero_moment = pic4['m00']
    # готовим координаты центроида
    x, y = None, None
    #Если найдены зеленые точки, то мы ищем центр фигуры зеленых, состоящей из зеленых точек

    if zero_moment != 0:
        x = int(pic4['m10']/zero_moment)#сумма Х координат точек/на кол-во точек
        y = int(pic4['m01']/zero_moment)#сумма Y координат точек/на кол-во точек

    # Предположим, что нет центроида
    coords = None

    # если функция нашла центроид, то возвращаем его координаты
    if x != None and y != None:
        coords = (x, y)
    return coords

sim.simxFinish(-1)

clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)



if clientID!=-1:
  print('Подключено к серверу')

  # получить объекты датчика зрения
  res, v0 = sim.simxGetObjectHandle(clientID, 'Vision_sensor', sim.simx_opmode_oneshot_wait)
  res, v1 = sim.simxGetObjectHandle(clientID, 'image', sim.simx_opmode_oneshot_wait)

  err, resolution, pic = sim.simxGetVisionSensorImage(clientID, v0, 0, sim.simx_opmode_streaming)
  time.sleep(1)

  while (sim.simxGetConnectionId(clientID) != -1):
    # получение изображения с датчика зрения "v0"
    err, resolution, pic = sim.simxGetVisionSensorImage(clientID, v0, 0, sim.simx_opmode_buffer)

    if err == sim.simx_return_ok:
      byte_array = array.array('b', pic)
      byte=bytes(byte_array)
      #Создаем память изображения, ссылающуюся на пиксельные данные в байтовом буфере 
      pixel_buff = I.frombuffer("RGB", (resolution[0],resolution[1]), byte, "raw", "RGB", 0, 1)

      img = numpy.asarray(pixel_buff)

      # попробуй найти что-нибудь зеленое
      ret = search_green(img)
      ret2 = search_red(img)
      ret3 = search_blue(img)
      rad_cube = 20
      flage1 = True

      # наложить маркер прямоугольника, если что-то найдено с помощью OpenCV
      if ret:
        cv2.rectangle(img,(ret[0]-rad_cube,ret[1]-rad_cube), (ret[0]+rad_cube,ret[1]+rad_cube), (0xff,0xff,0xff), 1)
        if flage1:
          sim.simxSetFloatSignal(clientID,'green',1,sim.simx_opmode_oneshot)
          sim.simxAddStatusbarMessage(clientID,"green",sim.simx_opmode_oneshot)

      if ret2:
        cv2.rectangle(img,(ret2[0]-rad_cube,ret2[1]-rad_cube), (ret2[0]+rad_cube,ret2[1]+rad_cube), (0xff,0xff,0xff), 1)
        if flage1:
          sim.simxSetFloatSignal(clientID,'green',2,sim.simx_opmode_oneshot)
          sim.simxAddStatusbarMessage(clientID,"red",sim.simx_opmode_oneshot)
      
      if ret3:
        cv2.rectangle(img,(ret3[0]-rad_cube,ret3[1]-rad_cube), (ret3[0]+rad_cube,ret3[1]+rad_cube), (0xff,0xff,0xff), 1)
        if flage1:
          sim.simxSetFloatSignal(clientID,'green',3,sim.simx_opmode_oneshot)
          sim.simxAddStatusbarMessage(clientID,"blue",sim.simx_opmode_oneshot)

      # вернуть изображение
      img = img.ravel()
      sim.simxSetVisionSensorImage(clientID, v1, img, 0, sim.simx_opmode_oneshot)
    
    elif err == sim.simx_return_novalue_flag:
      print("Нет картинки")
      pass
    else:
      print(err)
else:
  print("Ошибка подключения к серверу")
  sim.simxFinish(clientID)