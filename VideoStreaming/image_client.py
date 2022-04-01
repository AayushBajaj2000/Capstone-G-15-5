import cv2
import imagezmq
import numpy as np
image_hub = imagezmq.ImageHub('tcp://192.168.192.11:5555')

while True:  # show streamed images until Ctrl-C
    rpi_name, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)
    # see opencv docs for info on -1 parameter
    cv2.imshow(rpi_name, image)  # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')