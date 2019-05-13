import ctypes
import numpy as np
import asyncio
import websockets

np.set_printoptions(suppress=True)

m = ctypes.cdll.LoadLibrary('./lsm9ds0.so')
# m.py_readAccel.restype = c_float

m.py_readAccel.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_float, shape=(6,))

async def hello(websocket, path):
  name = await websocket.recv()

  while(True):
      output = m.py_readAccel().tolist()
      print(output)
      print(type(output))
      obj = []
      for i in output:
          obj.append(str(i))
      print(obj)
      await websocket.send(obj[0])

start_server = websockets.serve(hello, '192.168.7.2', 8675)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
