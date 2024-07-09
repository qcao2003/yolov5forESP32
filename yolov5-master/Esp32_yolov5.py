import cv2
import torch
import numpy as np
import socket
camera_url = "http://192.168.0.172:81/stream"
send_msg = "found"
# 创建socket对象
socket_client = socket.socket()
# 连接到服务器
socket_client.connect(("192.168.0.172", 1234))
# 读取yolov5模型
model = torch.hub.load('./', 'custom', path='yolov5s.pt', source='local', device='cpu')
# 设置模型
model.conf = 0.4

cap = cv2.VideoCapture(camera_url)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    img_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(img_cvt)
    # 打印得到的数据
    # print(str(results.pandas().xyxy[0].to_numpy()[:, -1]))  # tensor-to-numpy

    results_ = results.pandas().xyxy[0].to_numpy()
    for result in results_:
        target = result[6]
        if target == "person":
            #发送消息
            socket_client.send(send_msg.encode("UTF-8"))
        print(target)
    i = 0
    # 画图
    for box in results_:
        l, t, r, b = box[:4].astype('int')
        confidence = str(round(box[4] * 100, 2)) + "%"
        cls_name = box[6]
        cv2.rectangle(frame, (l, t), (r, b), (0, 200, 55), 2)
        cv2.putText(frame, cls_name + "-" + confidence, (l, t), cv2.FONT_ITALIC, 1, (200, 55, 0), 2)

    cv2.imshow("result", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
# 关闭连接
socket_client.close()