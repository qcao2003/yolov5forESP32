import cv2
import torch
import time
import numpy as np
import pickle
import struct
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
#被访问才往下执行
server_socket.listen(10)
# 获得client_socket的地址
client_socket, addr = server_socket.accept()
# 获得连接
connection = client_socket.makefile('wb')
# 读取yolov5模型
model = torch.hub.load('./', 'custom', path='yolov5s.pt', source='local', device='cpu')
# 设置模型
model.conf = 0.4

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    img_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(img_cvt)
    # 打印得到的数据
    print(str(results.pandas().xyxy[0].to_numpy()[:, -1]))  # tensor-to-numpy
    results_ = results.pandas().xyxy[0].to_numpy()
    i = 0
    # 画图
    for box in results_:
        l, t, r, b = box[:4].astype('int')
        confidence = str(round(box[4] * 100, 2)) + "%"
        cls_name = box[6]
        cv2.rectangle(frame, (l, t), (r, b), (0, 200, 55), 2)
        cv2.putText(frame, cls_name + "-" + confidence, (l, t), cv2.FONT_ITALIC, 1, (200, 55, 0), 2)
    data = pickle.dumps(frame)
    size = struct.pack('L', len(data))
    #数据传输
    connection.write(size)
    connection.write(data)
    # cv2.imshow("result", frame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
connection.close()
server_socket.close()