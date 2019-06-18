import ctypes
import numpy as np
import asyncio
import websockets
import time

np.set_printoptions(suppress=True)

m = ctypes.cdll.LoadLibrary('./lsm9ds0.so')
gpio = ctypes.cdll.LoadLibrary('./gpio.so')

m.py_readAccel.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_float, shape=(6,))

async def light():
  print('light_on')
  
  gpio.open_pin()
  print('turn_on')
  gpio.turn_on()
  await asyncio.sleep(0.5)
  print('turn_off')
  gpio.turn_off()
  print('light_off')
  #gpio.close_pin()



async def hello(websocket, path):
  name = await websocket.recv()

  while(True):
      output = m.py_readAccel().tolist()
      #print(output)
      #print(type(output))
      obj = []
      for i in output:
          obj.append(str(i))
      #print(obj)
      await websocket.send(obj[0])
      #time.sleep(1)
      
      hit = await websocket.recv()
      if hit == '1':
        await light()



start_server = websockets.serve(hello, '192.168.7.2', 8675)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
