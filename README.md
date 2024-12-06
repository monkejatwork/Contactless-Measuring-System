# Object Dimension Measurement Using OpenCV

This project uses **OpenCV** to measure the dimensions of an object in millimeters from a live webcam feed. By capturing an image, detecting the object's edges, and calculating its bounding box, the project outputs the object's width and height. It assumes the input image has a known DPI (dots per inch) for accurate conversion to millimeters.

---

## Features

1. **Real-Time Webcam Feed**:
   - Captures frames from a live webcam feed.
   - Displays the live video stream with options to capture an image.

2. **Object Measurement**:
   - Detects the largest object in the captured image using edge detection.
   - Calculates the object's dimensions in millimeters using the specified DPI.
   - Displays the object's outline and dimensions on the image.

3. **User Interaction**:
   - Press `c` to capture an image and measure the object's dimensions.
   - Press `q` to quit the application.

---

## Prerequisites

- **Python 3.6+**
- **OpenCV** (`cv2`)
- **NumPy**

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Sivarish04/object-dimension-measurement.git
   cd object-dimension-measurement
   ```

2. Install dependencies:
   ```bash
   pip install opencv-python numpy
   ```

3. Run the script:
   ```bash
   python CMScv7.py
   ```

4. Interact with the application:
   - **Press `c`**: Capture the current frame and calculate the object's dimensions.
   - **Press `q`**: Quit the application.

---

## Code Explanation

1. **Webcam Initialization**:
   - The webcam feed is started using `cv2.VideoCapture(0)`.
   - The resolution is set to `1280x720` for better accuracy.

2. **Object Measurement**:
   - The object is detected using the **Canny Edge Detection** method.
   - Contours are extracted to find the largest object in the frame.
   - A bounding rectangle is drawn around the detected object.
   - Dimensions are calculated in millimeters using the formula:
     \[
     \text{Size in mm} = \frac{\text{Size in pixels}}{\text{DPI} / 25.4}
     \]

3. **Visualization**:
   - The object's outline and dimensions are displayed on the image.
   - The dimensions are printed in the console.

4. **User Interaction**:
   - Press `c` to capture and measure.
   - Press `q` to quit.

---

## Example Output

When capturing an object:

1. **Console Output**:
   ```
   Width: 50.24 mm, Height: 120.48 mm
   ```

2. **Image Display**:
   - The object's outline is shown.
   - Dimensions are overlayed on the image.

---

## Customization

- **DPI**: Adjust the DPI value to match the input image's DPI for accurate results.
- **Resolution**: Change the webcam resolution to enhance accuracy.
- **Edge Detection**: Modify `cv2.Canny` thresholds for better edge detection.

---

## Limitations

1. Assumes the object is the largest contour in the frame.
2. Accurate results depend on the correct DPI setting.
3. Suitable for rectangular objects; irregular shapes may have errors.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
