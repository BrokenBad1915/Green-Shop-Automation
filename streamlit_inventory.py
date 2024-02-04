# import os
# import shutil

# def copy_all_images(source_folder, target_folder, starting_count):
#     # Creating target folder if it doesn't exist
#     os.makedirs(target_folder, exist_ok=True)

#     count = starting_count

#     for root, dirs, files in os.walk(source_folder):
#         for file in files:
#             if file.lower().endswith(('.png', '.jpg', '.jpeg')):
#                 source_path = os.path.join(root, file)
#                 target_path = os.path.join(target_folder, f"image_{count}.jpg")

#                 # Check if the target file already exists, and increment count if needed
#                 while os.path.exists(target_path):
#                     count += 1
#                     target_path = os.path.join(target_folder, f"image_{count}.jpg")

#                 shutil.copyfile(source_path, target_path)

#                 count += 1

#     return count

# def main():
#     # Set the desired parameters
#     source_folders = ['Mixed_Fruit2', 'Mixed_Fruit3', 'Mixed_Fruit4', 'Mixed_Fruit5', 'Mixed_Fruit6', 'Mixed_Fruit7', 'Mixed_Fruit8', 'Mixed_Fruit9', 'Mixed_Fruit10', 'Mixed_Fruit11', 'Mixed_Fruit12', 'Mixed_Fruit13', 'Mixed_Fruit14', 'Mixed_Fruit15']
#     target_folder = "Mixed_Fruit1"
#     starting_count = 1

#     # Copy all images from source folders to target folder
#     for source_folder in source_folders:
#         starting_count = copy_all_images(source_folder, target_folder, starting_count)

#     print(f"Image copy complete. Target folder: {target_folder}")

# if __name__ == "__main__":
#     main()



import streamlit as st
import os
import subprocess
import cv2
from PIL import Image

# Function to open camera and collect samples
def open_camera(product_name, weight_ordered, quantity):
    st.subheader("Camera")
    st.write("Please look into the camera and collect samples.")

    camo_device_id = 1
    cam = cv2.VideoCapture(camo_device_id)

    if not cam.isOpened():
        st.error("Error: Could not open camera device.")
        return

    count = 0
    folder_path = os.path.join(os.getcwd(), product_name.replace(" ", "_"))  # Creating folder path with product name
    os.makedirs(folder_path, exist_ok=True)  # Creating folder if it doesn't exist

    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Error: Couldn't read frame.")
            break

        count += 1
        face = cv2.resize(frame, (200, 400))

        file_name_path = os.path.join(folder_path, f"image_{count}.jpg")  # Creating file path with count
        cv2.imwrite(file_name_path, face)

        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Face Cropper', face)

        if cv2.waitKey(1) == 13 or count == 1:
            break

    cam.release()
    cv2.destroyAllWindows()
    st.success("Collecting Samples Complete")

# Function to open another Python file
def open_another_file():
    st.subheader("Green Shop Automation")
    subprocess.Popen(["streamlit", "run", "streamlit_checkout.py"])

# Main function
def main():
    st.set_page_config(page_title="Inventory Management", page_icon="📦")
    st.title("Inventory Management")

    # Text input for product name
    product_name = st.text_input("Enter the name of the product:")

    # Number input for amount of weight ordered
    weight_ordered = st.number_input("Amount of weight ordered (kg):", min_value=0.0)

    # Number input for approximate quantity
    quantity = st.number_input("Approximate quantity of the product:", min_value=0, step=1)

    # Button to open camera
    if st.button("Open Camera"):
        if product_name:
            open_camera(product_name, weight_ordered, quantity)
        else:
            st.error("Please enter the name of the product.")

    # Button to open another Python file
    if st.button("Go to checkout page"):
        open_another_file()

if __name__ == "__main__":
    main()





