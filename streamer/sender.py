import base64
import cv2
import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('[INFO] Successfully connected to server.')


@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')


@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')
    
    
def convert_image_to_jpeg(image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)
sio.connect('http://119.82.135.244:5001')
camera = cv2.VideoCapture(0)

def main():
    _last_update_t =0
      # init the camera
    while True:
        try:
            cur_t = time.time()
            if cur_t - _last_update_t > 0.2:
                _last_update_t = cur_t
                grabbed, frame = camera.read()  # grab the current frame
                frame = cv2.resize(frame, (640, 480))  # resize the frame
                # cv2.imshow('streamer', frame) 
                #encoded, buffer = cv2.imencode('.jpg', frame)
                #jpg_as_text = base64.b64encode(buffer)
               
                # footage_socket.send(jpg_as_text)
                sio.emit('cv2server',{'image': convert_image_to_jpeg(frame),'text': '<br /> Camera1'})
        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()
            break
 
if __name__ == "__main__":
    main()