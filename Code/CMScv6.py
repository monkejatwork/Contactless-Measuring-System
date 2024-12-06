import cv2
import numpy as np

# Function to compute the midpoint between two points
def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))

# Function to measure the dimensions of the object in an image
def measure_object(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection on the entire image
    edged = cv2.Canny(gray, 50, 150)

    # Find contours from the edged image
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming you want dimensions of the rectangle)
        c = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(c)

        # Draw the bounding box on the original frame (optional)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color

        # Conversion factor (500 pixels = 13 cm)
        pixels_to_cm = 13 / 500

        # Calculate width and height in centimeters
        width_cm = w * pixels_to_cm
        height_cm = h * pixels_to_cm

        # Create a white image with the same dimensions as the original (for measurements)
        white_image = np.ones(image.shape) * 255

        # Draw the contour on the white image
        cv2.drawContours(white_image, [c], -1, (0, 0, 0), 2)

        # Create reference points for dimension annotation
        p1 = (x, y)
        p2 = (x + w, y)
        p3 = (x, y + h)

        # Annotate width dimension (on white image)
        cv2.putText(white_image, f"{width_cm:.2f} cm", midpoint(p1, p2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.arrowedLine(white_image, p1, p2, (0, 0, 0), 1, tipLength=0.1)

        # Annotate height dimension (on white image)
        cv2.putText(white_image, f"{height_cm:.2f} cm", midpoint(p1, p3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.arrowedLine(white_image, p1, p3, (0, 0, 0), 1, tipLength=0.1)

        # Display the image with bounding box on original frame and contour with measurements on white background
        cv2.imshow("Original with Bounding Box", image)
        cv2.imshow("Contour and Measurements", white_image)
        cv2.waitKey(0)  # Wait for a key press to close the window

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

    # Display the current frame
    cv2.imshow("Webcam", frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If 'c' is pressed, capture the image and measure the object
    if key == ord('c'):
        # Save the captured image
        cv2.imwrite("captured_image.jpg", frame)

        # Measure object dimensions in the captured image
        measure_object(frame)  # Pass the captured frame directly

    # Press 'q' to quit the video stream
    if key == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()