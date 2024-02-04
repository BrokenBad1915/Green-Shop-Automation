# import cv2
# import numpy as np
# import os
# import re

# def natural_sort(l):
#     """Sort a list in natural order, considering numerical parts of strings."""
#     convert = lambda text: int(text) if text.isdigit() else text.lower()
#     alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
#     return sorted(l, key=alphanum_key)

# def detect_fruit_borders_in_cropped_image(image_path, output_path):
#     # Load the image
#     image = cv2.imread(image_path)

#     # Calculate cropping coordinates
#     image_height = image.shape[0]
#     desired_cropping_amount = 90  # Adjust as needed
#     center_y = image_height // 2
#     top_y = center_y - desired_cropping_amount +5
#     bottom_y = center_y + desired_cropping_amount -40

#     # Crop the image
#     cropped_image = image[top_y:bottom_y, 20:180]  # Adjust width coordinates as needed

#     # Proceed with fruit border detection
#     hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
#     lower_bounds = np.array([0, 50, 50])
#     upper_bounds = np.array([30, 255, 255])
#     mask = cv2.inRange(hsv, lower_bounds, upper_bounds)
#     kernel = np.ones((5, 5), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Draw bounding boxes around fruit contours in the cropped image
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         cv2.rectangle(cropped_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

#     # Get the base filename without extension
#     filename = os.path.basename(image_path).split('.')[0]

#     # Save the cropped image with borders
#     cv2.imwrite(os.path.join(output_path, f"{filename}_cropped.jpg"), cropped_image)

# # Define input and output paths
# input_folder = r'C:\Users\ronit\OneDrive\Documents\GitHub\Green-Shop-Automation\image_data\Orange'
# output_folder = r'C:\Users\ronit\OneDrive\Documents\GitHub\Green-Shop-Automation\boundary_image_data\Orange'

# # Create the output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# # Get a list of image filenames in the input folder
# image_filenames = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

# image_filenames = natural_sort(image_filenames)

# # Process the first 100 images
# for filename in image_filenames[300:500]:  # Slice the list to get the first 100
#     image_path = os.path.join(input_folder, filename)
#     detect_fruit_borders_in_cropped_image(image_path, output_folder)

import cv2
import numpy as np

def detect_fruit_borders_in_cropped_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Calculate cropping coordinates
    image_height = image.shape[0]
    desired_cropping_amount = 150  # Adjust as needed
    center_y = image_height // 2
    top_y = center_y - desired_cropping_amount
    bottom_y = center_y + desired_cropping_amount

    # Adjust for apple position (if needed)
    # Example: If the apple is slightly higher, adjust top_y upwards slightly

    # Crop the image
    cropped_image = image[top_y:bottom_y, :]  # Adjust width coordinates as needed
    print(cropped_image.shape)

    # Proceed with fruit border detection
    hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
    lower_bounds = np.array([0, 50, 50])
    upper_bounds = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_bounds, upper_bounds)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around fruit contours in the cropped image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(cropped_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the result of the cropped image with borders
    cv2.imshow('Cropped Image with Fruit Borders', cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Path to your image
image_path = r'C:\Users\ronit\OneDrive\Documents\GitHub\Green-Shop-Automation\Mixed_Fruit1\image_1.jpg'

# Detect fruit borders in the cropped image
detect_fruit_borders_in_cropped_image(image_path)