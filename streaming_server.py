from flask import Flask, Response, request
import logging
import cv2
from threading import Thread, Lock
import time
from waitress import serve
import os

# Function to scan and select the video source
def select_camera():
    max_cameras = 10
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available_cameras.append(i)
            cap.release()

    if not available_cameras:
        raise Exception("No cameras found.")

    print("Available cameras:", available_cameras)
    camera_index = int(input("Select camera index: "))
    if camera_index not in available_cameras:
        raise ValueError(f"Invalid camera index: {camera_index}")

    return camera_index

# Call the camera selection function before starting the server
camera_index = select_camera()

os.system('cls')
print(r"""
   _____                     _         _____ _                            
  / ____|                   (_)       / ____| |                           
 | |     ___  _ __ ___  __ _ _ _ __  | (___ | |_ _ __ ___  __ _ _ __ ___  
 | |    / _ \| '__/ __|/ _` | | '__|  \___ \| __| '__/ _ \/ _` | '_ ` _ \ 
 | |___| (_) | |  \__ \ (_| | | |     ____) | |_| | |  __/ (_| | | | | | |
  \_____\___/|_|  |___/\__,_|_|_|    |_____/ \__|_|  \___|\__,_|_| |_| |_|
          
---------------------------STREAMING ON PORT 5000---------------------------
""")


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Global camera and lock for thread safety
camera = cv2.VideoCapture(0)
camera_lock = Lock()

def gen_frames(): 
    while True:
        with camera_lock:
            success, frame = camera.read()
            if not success:
                break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.05)  # Introduce a slight delay to reduce server load

@app.route('/video_feed')
def video_feed():
    client_ip = request.remote_addr
    app.logger.info(f"Connection requested from {client_ip}")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<html><body><img src='/video_feed'></body></html>"

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
    
