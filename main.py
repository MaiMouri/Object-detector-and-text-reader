from distutils import command
import os
from google.cloud import texttospeech
from google.oauth2 import service_account

import io
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'


def data_transport(words):
    input_data = words
    print('done')
    st.write('data')
    st.write(input_data)
    st.markdown('### parameter settings')

    lang = st.selectbox('Language', ('日本語', '英語'))
    gender = st.selectbox('Gender', ('male', 'female', 'neutral'))

    st.write('### Create voice')
    if st.button('Start'):
        comment = st.empty()
        comment.write('Creating the voice...')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        st.audio(response.audio_content)
        comment.write('Complete!')


def synthesize_speech(text, lang='英語', gender='default'):
    gender_type = {
        'defalut': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }
    lang_code = {'英語': 'en-US', '日本語': 'ja-JP'}
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=lang_code[lang],
                                              ssml_gender=gender_type[gender])
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input,
                                        voice=voice,
                                        audio_config=audio_config)
    return response


# lang = '英語'
# gender = 'default'
# text = "Hello, World!"

# response = synthesize_speech(text, gender='male')

# st.title('Text-to-Speech')
# st.markdown('### Voice-text')

input_data = None

if input_data is not None:
    st.write('data')
    st.write(input_data)
    st.markdown('### parameter settings')

    lang = st.selectbox('Language', ('日本語', '英語'))
    gender = st.selectbox('Gender', ('male', 'female', 'neutral'))

    st.write('### Create voice')
    if st.button('Start'):
        comment = st.empty()
        comment.write('Creating the voice...')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        st.audio(response.audio_content)
        comment.write('Complete!')
