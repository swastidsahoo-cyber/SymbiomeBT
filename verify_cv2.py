import cv2
import os

try:
    print(f"CV2 Version: {cv2.__version__}")
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    print(f"Looking for Haarcascade at: {path}")
    
    if os.path.exists(path):
        print("SUCCESS: XML File Found.")
        clf = cv2.CascadeClassifier(path)
        if not clf.empty():
            print("SUCCESS: CascadeClassifier Loaded.")
        else:
            print("FAILURE: CascadeClassifier Empty.")
    else:
        print("FAILURE: XML File NOT Found.")
        
except Exception as e:
    print(f"FAILURE: {e}")
