import cv2
import numpy as np

# Function to compute the midpoint between two points
def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))

# Function to measure the dimensions of the object in an image
def measure_object(image_path):
    try:
        # Read the image
        img = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Use Canny edge detection on the entire image
        edged = cv2.Canny(gray, 50, 150)

        # Find contours from the edged image
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour (assuming you want dimensions of the rectangle)
            c = max(contours, key=cv2.contourArea)

            # Get the bounding rectangle of the largest contour
            x, y, w, h = cv2.boundingRect(c)

            # Conversion factor (500 pixels = 13 cm)
            pixels_to_cm = 13 / 500

            # Calculate width and height in centimeters
            width_cm = w * pixels_to_cm
            height_cm = h * pixels_to_cm

            # Create reference points for dimension annotation
            p1 = (x, y)
            p2 = (x + w, y)
            p3 = (x, y + h)

            # Annotate width dimension
            cv2.putText(edged, f"{width_cm:.2f} cm", midpoint(p1, p2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.arrowedLine(edged, p1, p2, (255, 255, 255), 1, tipLength=0.1)

            # Annotate height dimension
            cv2.putText(edged, f"{height_cm:.2f} cm", midpoint(p1, p3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.arrowedLine(edged, p1, p3, (255, 255, 255), 1, tipLength=0.1)

        # Display the image with edges and measurements
        cv2.imshow("Original Image", img)
        cv2.imshow("Canny Edges with Measurements", edged)
        cv2.waitKey(0)  # Wait for a key press to close the windows

    except Exception as e:
        print(f"Error: {e}")

# Specify the image path
image_path = "/home/sivarish04/C:Folder/project/CMS/Properties-of-Rectangle.webp"

# Measure object dimensions in the image
measure_object(image_path)

# Close all windows
cv2.destroyAllWindows()