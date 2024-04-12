import cv2
import serial

# Open serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port and baud rate as needed

# Open laptop camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Perform object detection or any other processing here
    
    # Simplified example: Detect if object is present
    object_present = detect_object(frame)
    
    # Send object presence status to Arduino
    ser.write(b'1' if object_present else b'0')
