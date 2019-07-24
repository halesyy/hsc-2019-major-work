import numpy as np
arr = np.array([
  [[255,255,255], [255,255,255], [0,0,0]],
  [[255,255,255], [0,0,0], [0,0,0]],
  [[0,0,0], [0,0,0], [0,0,0]]
]);
# arr = np.array([0, 0, 0])

print(arr.flatten())
f = arr.flatten()
if 255 in f:
    print("oh no!")
else:
    print("oh yeah ;)")

# t = np.where(arr == 255)
# print(t)
