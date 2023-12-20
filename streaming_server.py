from flask import Flask, Response, request
import logging
import cv2
from threading import Thread, Lock
import time
from waitress import serve
import os

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
    # Enable threading in Flask
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
    serve(app, host='0.0.0.0', port=5000)
    
