# # checkout.py
# import streamlit as st
# import cv2

# def main():
#     st.set_page_config(page_title="Checkout", page_icon="💳")
#     st.title("Checkout")

#     # Initialize OpenCV camera
#     cam = cv2.VideoCapture(0)

#     # Placeholder text while camera is starting
#     st.write("Initializing camera...")

#     # Function to read frame from camera
#     def read_frame():
#         ret, frame = cam.read()
#         if not ret:
#             st.error("Error: Couldn't read frame.")
#             return None
#         return frame

#     # Divide the layout into two columns: 70% for camera and 30% for bill
#     col1, col2 = st.columns([7, 3])

#     # Display live camera feed in the first column
#     with col1:
#         st.subheader("Live Camera Feed")
#         stframe = st.empty()
#         while True:
#             frame = read_frame()
#             if frame is None:
#                 break
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
#             stframe.image(frame, channels="RGB")

#     # Display bill section in the second column
#     with col2:
#         st.subheader("Bill")
#         # Add code to display bill section here

# if __name__ == "__main__":
#     main()


import streamlit as st
import cv2
import requests

# API credentials (replace with your own)
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}

# Price dictionary for identified fruits (update with your prices)
fruit_prices = {"apple": 1.50, "banana": 0.75, "orange": 1.25}  # Add more fruits and prices

def query(frame):
    _, frame_encoded = cv2.imencode(".jpg", frame)
    data = frame_encoded.tobytes()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def cnt(output):
    cost = {}
    for x in output:
        if x["label"] in cost:
            cost[x["label"]] += 1
        else:
            cost[x["label"]] = 1
    return cost

def main():
    st.set_page_config(page_title="Checkout", page_icon="")
    st.title("Checkout")

    cam = cv2.VideoCapture(0)  # Use 0 for default camera
    st.write("Initializing camera...")

    bill_items = {}  # Dictionary to store bill items
    total_bill = 0.0

    def display_camera():
        frame_count = 0
        fps = cam.get(cv2.CAP_PROP_FPS)

        while True:
            frame = read_frame()
            if frame is None:
                break

            # Send frame for identification every 2 seconds
            if frame_count % (int(fps * 2)) == 0:
                identified_fruits = query(frame)
                # update_bill(identified_fruits)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame, channels="RGB")
            frame_count += 1

    def read_frame():
        ret, frame = cam.read()
        return frame

    # def update_bill(identified_fruits):
    #     global total_bill
    #     for fruit, count in cnt(identified_fruits).items():
    #         if fruit in fruit_prices:
    #             price = fruit_prices[fruit]
    #             if fruit in bill_items:
    #                 bill_items[fruit]["quantity"] += count
    #             else:
    #                 bill_items[fruit] = {"quantity": count, "price": price}
    #             total_bill += price * count

    # Streamlit layout
    col1, col2 = st.columns([7, 3])

    with col1:
        st.subheader("Live Camera Feed")
        stframe = st.empty()
        if st.button("Start Camera"):
            display_camera()

    with col2:
        st.subheader("Bill")
        for item, details in bill_items.items():
            st.write(f"{item}: {details['quantity']} x ${details['price']:.2f}")
        st.write("-" * 10)
        st.write(f"Total: ${total_bill:.2f}")

    # Release camera upon exiting
    cam.release()

if __name__ == "__main__":
    main()


