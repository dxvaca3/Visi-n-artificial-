import cv2
import numpy as np
import time
import serial

cv2.namedWindow("Camara Original", cv2.WINDOW_NORMAL)
cv2.namedWindow("Solo Azul", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mascara", cv2.WINDOW_NORMAL)

# ========= SERIAL =========
COM = 'COM3'        # CAMBIA según tu sistema
BAUD = 9600
ser = serial.Serial(COM, BAUD, timeout=1)
time.sleep(2)

# ========= CAMARA =========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ========= TIEMPO =========
prev_time = time.time()
frame_count = 0

# ========= HSV AZUL =========
lower_blue = np.array([100, 150, 50])
upper_blue = np.array([141, 255, 255])

# ========= CENTROS =========
CENTER_X = 320
CENTER_Y = 240

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask_blue)

    ys, xs = np.where(mask_blue == 255)

    if len(xs) > 0:
        cx = int(xs.mean())
        cy = int(ys.mean())

        cv2.putText(frame,
                    f"x={cx}, y={cy}, FPS={int(fps)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2)

        # ===== EJE X =====
        if cx < 200:
            ser.write(b"izq1\n")
        elif 260 > cx >= 200:
            ser.write(b"izq2\n")
        elif 300 > cx >= 260:
            ser.write(b"izq3\n")
        elif 340 >= cx >= 300:
            ser.write(b"ctrX\n")
        elif 380 >= cx > 340:
            ser.write(b"der3\n")
        elif 440 >= cx > 380:
            ser.write(b"der2\n")
        else:
            ser.write(b"der1\n")

        # ===== EJE Y =====
        if cy < 140:
            ser.write(b"up1\n")
        elif 190 > cy >= 140:
            ser.write(b"up2\n")
        elif 220 > cy >= 190:
            ser.write(b"up3\n")
        elif 260 >= cy >= 220:
            ser.write(b"ctrY\n")
        elif 290 >= cy > 260:
            ser.write(b"down3\n")
        elif 340 >= cy > 290:
            ser.write(b"down2\n")
        else:
            ser.write(b"down1\n")

    # ===== RECALIBRACIÓN HSV =====
    if frame_count % 30 == 0:
        pixels = hsv[mask_blue == 255]
        if len(pixels) > 50:
            h_mean = np.mean(pixels[:, 0])
            s_mean = np.mean(pixels[:, 1])
            v_mean = np.mean(pixels[:, 2])

            lower_blue = np.array([
                max(0, h_mean - 10),
                max(50, s_mean - 40),
                max(50, v_mean - 40)
            ], dtype=np.uint8)

            upper_blue = np.array([
                min(180, h_mean + 10),
                255,
                255
            ], dtype=np.uint8)

    cv2.imshow("Camara Original", frame)
    cv2.imshow("Solo Azul", result)
    cv2.imshow("Mascara", mask_blue)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()