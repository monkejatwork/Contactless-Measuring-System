import cv2
import numpy as np

def measure_object(image, dpi=300):
    """Measures the dimensions of the object in an image in millimeters.

    Args:
        image (np.ndarray): Input image.
        dpi (int): Dots per inch (DPI) of the image.

    Returns:
        tuple: (width in mm, height in mm)
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection on the entire image
    edged = cv2.Canny(gray, 50, 150)

    # Find contours from the edged image
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming you want dimensions of the rectangle)
        c = max(contours, key=cv2.contourArea)

        # Create a white image with the same dimensions as the original (for visualization)
        white_image = np.ones(image.shape) * 255

        # Draw the contour on the white image (outline visualization)
        cv2.drawContours(white_image, [c], -1, (0, 0, 0), 2)  # Black color

        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)

        # Calculate dimensions in millimeters
        width_mm = w / (dpi / 25.4)
        height_mm = h / (dpi / 25.4)

        # Format the text with dimensions
        text = f"Width: {width_mm:.2f} mm, Height: {height_mm:.2f} mm"
        cv2.putText(white_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Display the image with the outline and dimensions
        cv2.imshow("Object Outline with Dimensions", white_image)
        cv2.waitKey(0)  # Wait for a key press to close the window

        return width_mm, height_mm

    else:
        print("No contours found.")
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

    # Display the current frame
    cv2.imshow("Webcam", frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If 'c' is pressed, capture the image and measure the object
    if key == ord('c'):
        # Save the captured image
        cv2.imwrite("captured_image.jpg", frame)

        # Measure object dimensions in the captured image
        width_mm, height_mm = measure_object(frame, dpi=300)  # Assuming 300 DPI
        if width_mm is not None and height_mm is not None:
            print(f"Width: {width_mm:.2f} mm, Height: {height_mm:.2f} mm")

    # Press 'q' to quit the video stream
    if key == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()