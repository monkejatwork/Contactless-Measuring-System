import cv2
import numpy as np

# Function to compute the midpoint between two points
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Function to measure the dimensions of the object
def measure_object(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)
        
        # Get the bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate width and height in pixels
        width_px = w
        height_px = h

        # Conversion factor (13 cm / 500 pixels)
        pixels_to_cm = 13 / 500

        # Convert to centimeters
        width_cm = width_px * pixels_to_cm
        height_cm = height_px * pixels_to_cm

        # Display the dimensions
        cv2.putText(frame, f"Width: {width_cm:.2f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Height: {height_cm:.2f} cm", (x, y + h + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return width_cm, height_cm

    return None, None

# Start the webcam capture
cap = cv2.VideoCapture(0)

# Set the resolution for better accuracy (if supported by the webcam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Measure object dimensions
    measure_object(frame)

    # Display the frame with the drawn rectangles and dimensions
    cv2.imshow("Object Dimensions Measurement", frame)

    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
