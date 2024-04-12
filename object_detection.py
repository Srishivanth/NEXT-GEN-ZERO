import numpy as np
import imutils
import cv2
import time
import serial

# Open serial connection to Arduino
ser = serial.Serial('COM4', 9600)

prototxt = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"
confThresh = 0.5

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "Human", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor", "mobile"]

MESSAGE_MAPPING = {
    "background": b'0',
    "aeroplane": b'1',
    "bicycle": b'2',
    "bird": b'3',
    "boat": b'4',
    "bottle": b'5',
    "bus": b'6',
    "car": b'7',
    "cat": b'8',
    "chair": b'9',
    "cow": b'10',
    "diningtable": b'11',
    "dog": b'12',
    "horse": b'13',
    "motorbike": b'14',
    "Human": b'h',
    "pottedplant": b'16',
    "sheep": b'17',
    "sofa": b'18',
    "train": b'19',
    "tvmonitor": b'20',
    "mobile": b'21'
}

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("Loading model.......")
net = cv2.dnn.readNetFromCaffe(prototxt, model)
print("Model Loaded")
print("Starting Camera Feed.....")

vs = cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    ret, frame = vs.read()
    frame = imutils.resize(frame, width=1000)
    (h, w) = frame.shape[:2]

    imResizeBlob = cv2.resize(frame, (300, 300))
    blob = cv2.dnn.blobFromImage(imResizeBlob, 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    detShape = detections.shape[2]
    object_present = False  # Initialize object presence flag

    for i in np.arange(0, detShape):
        confidence = detections[0, 0, i, 2]
        if confidence > confThresh:
            idx = int(detections[0, 0, i, 1])
            print("ClassID: ", detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{} : {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)

            if startY - 15 > 15:
                y = startY - 15
            else:
                y = startY + 15

            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            object_present = True  # Set object presence flag if object is detected

            # Send different messages to Arduino based on the detected object
            label = CLASSES[idx]
            message = MESSAGE_MAPPING.get(label, b'0')  # Get the corresponding message from the mapping
            print("Object Detected: ", label)
            print("Sending message to Arduino:", message)
            ser.write(message)

    cv2.imshow("frame", frame)
    
    # Send object presence status to Arduino
    if not object_present:
        ser.write(b'n')

    key = cv2.waitKey(1)
    if key == 27:
        break

vs.release()
cv2.destroyAllWindows()