import streamlit as st
import requests
import cv2
import os
import requests
# from gaze_tracking import GazeTracking


st.set_page_config(layout="wide")
col1, col2 = st.columns([0.3, 0.7])

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def cnt(output):
    # print(output)
    cost = {}
    for x in output:
        if x["label"] in cost:
            cost[x["label"]] +=1
        else:
            cost[x["label"]] =1
    return cost

def price(prediction):
    allowed=['apple','banana','orange']
    weight_dict={
        'apple':200,
        'banana':118,
        'orange':125
    }
    weight=0
    for i in prediction:
        if i in allowed:
            weight+=prediction[i]*weight_dict[i]
    return weight



def capture_video(old):
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    attention = [0, 0]
    # gaze = GazeTracking()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        
        path=os.path.join(os.getcwd(),'image.jpg')
        cv2.imwrite(path, frame)
        detection=cnt(query(path))
        output=''
        allowed=['apple','banana','orange']
        for i in detection:
            if i in allowed:
                output+=' '+f'{i}: {detection[i]}'
    
        cv2.putText(frame, output, (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,2550), 1, cv2.LINE_AA)

        frame_placeholder.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            channels="RGB",
            use_column_width=True,
        )

        with col1:
            print(output)
            if output!=old:
                st.write(price(detection))
        old=output

        if cv2.waitKey(1)  & 0xff==ord('q'):
            break
    cap.release()


    

with col2:
    st.subheader("Livestream")
    old=''
    capture_video(old)