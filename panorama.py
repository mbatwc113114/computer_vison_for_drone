import cv2
print("CUDA Device Count:", cv2.cuda.getCudaEnabledDeviceCount())
print("Has CUDA module?", hasattr(cv2, 'cuda'))
