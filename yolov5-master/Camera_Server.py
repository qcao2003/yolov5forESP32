import socket
import cv2
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(10)

client_socket, addr = server_socket.accept()

connection = client_socket.makefile('wb')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    last_img = cv2.circle(frame, center=(200, 200), radius=5, color=(255, 0, 3), thickness=6)
    data = pickle.dumps(last_img)
    size = struct.pack('L', len(data))

    #数据传输
    connection.write(size)
    connection.write(data)
    #本地显示
    # cv2.imshow('Camera', last_img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
connection.close()
server_socket.close()