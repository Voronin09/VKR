# simple_image_retranslate.py
#
# Demo of simple image retranslate from v0 to v1

# import sim
import time
import sim

sim.simxFinish(-1)

clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
  print ('Connected to remote API server')

  # get vision sensor objects
  res, v0 = sim.simxGetObjectHandle(clientID, 'v0', sim.simx_opmode_oneshot_wait)
  res, v1 = sim.simxGetObjectHandle(clientID, 'v1', sim.simx_opmode_oneshot_wait)


  err, resolution, image = sim.simxGetVisionSensorImage(clientID, v0, 0, sim.simx_opmode_streaming)
  time.sleep(1)

  while (sim.simxGetConnectionId(clientID) != -1):
    err, resolution, image = sim.simxGetVisionSensorImage(clientID, v0, 0, sim.simx_opmode_buffer)
    if err == sim.simx_return_ok:
      sim.simxSetVisionSensorImage(clientID, v1, image, 0, sim.simx_opmode_oneshot)
    elif err == sim.simx_return_novalue_flag:
      print ("no image yet")
    else:
      print (err)
else:
  print ("Failed to connect to remote API Server")
  sim.simxFinish(clientID)