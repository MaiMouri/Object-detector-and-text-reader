from threading import local
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import time
import json
import streamlit as st

import main

st.set_page_config(layout="wide")

# with open('secret.json') as f:
#     secret = json.load(f)
# KEY = secret['KEY']
# ENDPOINT = secret['ENDPOINT']
KEY = st.secrets.key
ENDPOINT = st.secrets.endpoint
computervision_client = ComputerVisionClient(ENDPOINT,
                                             CognitiveServicesCredentials(KEY))


## OCR
def read_words(filepath):
    local_image = open(filepath, "rb")
    read_response = computervision_client.read_in_stream(local_image, raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            words = []
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)
                words.append(line.text)
    print()
    return words


## Tags
def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name


## Detect the object( return the location )
def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results = computervision_client.detect_objects_in_stream(
        local_image)
    objects = detect_objects_results.objects
    return objects


placeholder = st.empty()
# プレースホルダにコンテナを追加する
container = placeholder.container()
# コンテナにカラムを追加する
col1, col2 = container.columns(2)
# それぞれのカラムに書き込む
with col1:
    # st.write('Hello, World')
    st.title("Object Detector")
    uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'png'])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img_path = f'img/{uploaded_file.name}'
        img.save(img_path)
        objects = detect_objects(img_path)

        draw = ImageDraw.Draw(img)
        for object in objects:
            x = object.rectangle.x
            y = object.rectangle.y
            w = object.rectangle.w
            h = object.rectangle.h
            caption = object.object_property

            font = ImageFont.truetype(font='./Helvetica.ttf', size=50)
            text_w, text_h = draw.textsize(caption, font=font)

            draw.rectangle([(x, y), (x + text_w, text_h + y)],
                           fill='green',
                           outline='green',
                           width=5)
            draw.text([x, y], caption, fill='white', font=font)
            draw.rectangle([(x, y), (x + w, h + y)],
                           fill=None,
                           outline='green',
                           width=5)
        st.image(img)

        tags_name = get_tags(img_path)
        tags_name = ', '.join(tags_name)
        st.markdown('Detected content tags')
        st.markdown(f'> {tags_name}')

with col2:
    # st.write('Konnichiwa, Sekai')
    st.title("Words Reader")
    words_file = st.file_uploader('Choose an image...',
                                  type=['jpg', 'png', 'jpeg'],
                                  key=['words'])
    if words_file is not None:
        words_img = Image.open(words_file)
        words_img_path = f'img/{words_file.name}'
        words_img.save(words_img_path)
        words = read_words(words_img_path)

        st.image(words_img)

        words = ', '.join(words)
        st.markdown('Words...')
        st.markdown(f'> {words}')

        main.data_transport(words)
