#!/usr/bin/python
import socket
import cv2
import numpy

# 연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = '192.168.1.112'
TCP_PORT = 5001

# 더미 imu값
imu = numpy.zeros((10))

# 송신을 위한 socket 준비
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 640)

cup = cv2.VideoCapture(2)
cup.set(3, 480)
cup.set(4, 640)

while True:
    cap.grab()
    cup.grab()
    ret, frame = cap.retrieve()
    ret2, frame2 = cup.retrieve()

    # 추출한 이미지를 String 형태로 변환(인코딩)시키는 과정
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    ret, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tobytes()

    ret, imgencode2 = cv2.imencode('.jpg', frame2, encode_param)
    data2 = numpy.array(imgencode2)
    stringData2 = data2.tobytes()

    # imu data 전송
    imuData = imu.tobytes()
    sock.send(imuData);

    # String 형태로 변환한 이미지를 socket을 통해서 전송
    sock.send(str(len(stringData)).ljust(16).encode());
    sock.send(str(len(stringData2)).ljust(16).encode());
    sock.send(stringData);
    sock.send(stringData2);

sock.close()
