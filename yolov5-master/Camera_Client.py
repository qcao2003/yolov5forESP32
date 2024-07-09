import socket
import cv2
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

connection = client_socket.makefile('rb')
cv2.namedWindow('Camera',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera', 1024, 768)
while True:
    size = struct.unpack('L', connection.read(struct.calcsize('L')))[0]
    data = connection.read(size)
    frame = pickle.loads(data)

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
connection.close()
client_socket.close()