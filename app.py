import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import cv2
from bargraph_driver import Setup
from driverfn_pie import setup
from production import predict
from PIL import Image
import os
import base64
from io import BytesIO
import webbrowser
from pathlib import Path

#st.set_option('deprecation.showfileUploaderEncoding', False)
#st.set_option('deprecation.showImageFormat', False)

st.title("Smarter Charts")
st.header("Please Upload the Image for Classification and Processing of Data.")
def category_is(str_pred):
    if str_pred is 'hg':
        st.write("The image contains a Bar Graph.")
    elif str_pred is 'pc':
        st.write("The image contains a Pie Chart.")
    
instructions = False
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file is not None and instructions is False:
    image = Image.open(uploaded_file)
    st.image(image, caption="Transformed Image…", channels="RGB", format="PNG", use_column_width=True)
    st.write("")
    st.write("Classifying...")
    class_pred=predict(uploaded_file)
    #st.write(class_pred[0])
    str_pred=str(class_pred)
    category_is(str_pred)
    dir_name=os.path.dirname(os.path.abspath(__file__))
    correct=st.button("It is correct?")
    output_name=st.text_input("Enter the name of the output Excel File without extension","IMAGE_DEFAULT")
    final_output_name=str(output_name)+str(".xlsx")
    if correct:
        cat=str_pred
        category_is(cat)
        if cat is 'hg':
            im1=image.save("Save.png")
            st.write("Now Computing...")
            st.write(uploaded_file)
            complete=Setup("Save.png",final_output_name)
            if complete:
                os.remove("Save.png")
                webbrowser.open_new_tab(dir_name+"/"+final_output_name)
                done=st.button("Is the viewing complete?")
                if done:
                    path=Path.cwd()
                    path=path/final_output_name
                    path.unlink()
                    
        elif cat is 'pc':
            im1=image.save("Save.png")
            st.write("Now Computing...")
            st.write(uploaded_file)
            complete=setup("Save.png",final_output_name)
            if complete:
                os.remove("Save.png")
                webbrowser.open_new_tab(dir_name+"/"+final_output_name)
                done=st.button("Is the viewing complete?")
                if done:
                    path=Path.cwd()
                    path=path/final_output_name
                    path.unlink()
            
                    

    
