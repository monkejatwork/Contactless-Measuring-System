import cv2
import numpy as np

# Function to compute the midpoint between two points
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Start the webcam capture
cap = cv2.VideoCapture(0)

# Set the resolution for better accuracy (if supported by the webcam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Known reference object width in millimeters (e.g., width of a reference object like a coin or a card)
reference_width_mm = 50.0  # Change this to the width of your known object (in mm)

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Apply edge detection
    edged = cv2.Canny(blurred, 50, 100)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area to identify the largest contour
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Process each contour
    for contour in contours:
        # Compute the rotated bounding box of the contour
        box = cv2.minAreaRect(contour)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # Draw the contour (for visualization)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

        # Compute the midpoints of the box edges
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # Compute the Euclidean distances between the midpoints (object width and height in pixels)
        width_pixels = np.linalg.norm([tltrX - blbrX, tltrY - blbrY])
        height_pixels = np.linalg.norm([tlblX - trbrX, tlblY - trbrY])

        # Compute pixels per millimeter using the known width of the reference object
        pixels_per_mm = width_pixels / reference_width_mm

        # Compute actual width and height of the object in millimeters
        actual_width_mm = width_pixels / pixels_per_mm
        actual_height_mm = height_pixels / pixels_per_mm

        # Print the dimensions in millimeters
        print(f"Width: {actual_width_mm:.2f} mm, Height: {actual_height_mm:.2f} mm")

        # Annotate the dimensions on the frame
        cv2.putText(frame, f"Width: {actual_width_mm:.1f} mm", (int(tltrX - 50), int(tltrY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Height: {actual_height_mm:.1f} mm", (int(tlblX - 100), int(tlblY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        break  # Process only the largest detected object

    # Display the frame with the drawn contours and dimensions
    cv2.imshow("Object Dimensions in mm", frame)

    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
