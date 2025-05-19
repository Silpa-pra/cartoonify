import streamlit as st
import cv2
import numpy as np 
from PIL import Image

#Title and Description
st.title("Image Cartoonifier")
st.write("Upload an image and choose a cartoon style to see the transformation!")

#Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file  is not None:
    #convert uploaded file to opencv format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    color_image =cv2.imdecode(file_bytes, 1)

    #Display original image
    st.subheader("Original Image")
    st.image(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB), caption= 'Original Image', use_container_width =True)

    #choose cartoon style
    cartoon_style_selection = st.selectbox("Select Cartoon Style", [
        "Smooth Watercolor",
        "Sharp Edges",
        "Realistic Sketch"
    ])

    if st.button("Apply Cartoon Effect"):
        if cartoon_style_selection == "Smooth Watercolor":
            cartoon_image = cv2.stylization(color_image, sigma_s=150, sigma_r=0.25)
        elif cartoon_style_selection == "Sharp Edges":
            cartoon_image = cv2.stylization(color_image, sigma_s=60, sigma_r=0.5)
        elif cartoon_style_selection == "Realistic Sketch":
            gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(color_image, 9, 250, 250)
            cartoon_image = cv2.bitwise_and(color, color, mask=edges)
        
        #Convert BGR to RGB for display
        cartoon_image_rgb = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2RGB)

        #show processed image
        st.header(f"Cartoonified Image - {cartoon_style_selection}")
        st.image(cartoon_image_rgb, caption=f'{cartoon_style_selection}', use_container_width =True)

        #Download button
        img_pil = Image.fromarray(cartoon_image_rgb)
        from io import BytesIO
        buf = BytesIO()
        img_pil.save(buf, format="PNG")
        byte_img =buf.getvalue()

        st.download_button(
            label= "Download Image",
            data= byte_img,
            file_name= "cartoonified_img.png",
            mime="image/png"
        )
else:
    st.warning("Please upload an image file.")