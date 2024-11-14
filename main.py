import cv2
import numpy as np
import streamlit as st
import tempfile
import os

st.title("Invisibility Cloak Effect")

st.write("""
Harry :  Hey !! Would you like to try my invisibility cloak ??
         It's awesome !!
         Prepare to get invisible .....................
""")

# Upload video file
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

# Parameters for red color detection
st.sidebar.header("Color Detection Parameters")
lower_hue = st.sidebar.slider("Lower Hue", 0, 180, 0)
upper_hue = st.sidebar.slider("Upper Hue", 0, 180, 10)
saturation = st.sidebar.slider("Saturation", 70, 255, 120)
value = st.sidebar.slider("Value", 70, 255, 70)

if uploaded_file is not None:
    # Save uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    
    # Open the video file with OpenCV
    cap = cv2.VideoCapture(video_path)
    
    # Capture the background from the first few frames
    ret, background = cap.read()
    if ret:
        background = np.flip(background, axis=1)
    
    # Prepare to save the output video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    output_path = os.path.join(tempfile.gettempdir(), 'output_invisible_cloak.mp4')
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect red color
        lower_red = np.array([lower_hue, saturation, value])
        upper_red = np.array([upper_hue, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([170, saturation, value])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = mask1 + mask2
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        
        # Replace red pixels with background pixels
        frame[np.where(mask == 255)] = background[np.where(mask == 255)]
        
        # Save frame to output video
        out.write(frame)

    cap.release()
    out.release()
    
    # Display the processed video
    st.video(output_path)

    # Provide a download link
    with open(output_path, "rb") as video_file:
        st.download_button(label="Download Output Video", data=video_file, file_name="output_invisible_cloak.mp4", mime="video/mp4")
