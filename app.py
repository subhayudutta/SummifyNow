import streamlit as st
import openai
from pytube import YouTube

openai.api_key=st.secrets['pass']

def summarize_written_text():
    st.title("Summarize Written Text")

    text = st.text_area("Enter text")
    temp = st.slider("Temperature", 0.0, 1.0, 0.5)

    if st.button("Generate"):
        if len(text)>100:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="Please summarize this article in a few points (points should be in 1,2,3,..): " + text,
                max_tokens=516,
                temperature=temp
            )

            res = response["choices"][0]["text"]
            st.info(res)
        else:
            st.warning("Cannot")
    

def summarize_audio():
    st.title("Summarize Audio")
    audio=st.file_uploader("Upload Audio",type=["wav","mp3","m4a","mp4"])
    st.text("Play audio")
    st.audio(audio)

    if st.button("Generate text"):
        if audio is not None:
            transcript = openai.Audio.transcribe("whisper-1", audio)
            st.info(transcript["text"])
        else:
            st.warning("Cannot")

    if st.button("Summarize Text"):
        if audio is not None:
            transcript = openai.Audio.transcribe("whisper-1", audio)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="Please summarize this article in a few points (points should be in 1,2,3,..): " + transcript["text"],
                max_tokens=516,
                temperature=0.5
            )
            res = response["choices"][0]["text"]
            st.info(res)
        else:
            st.warning("Cannot")



def summarize_youtube_video():
    st.title("Summarize YouTube Video")
    url=st.text_input("Enter YouTube Video Link")

    if st.button("Generate"):
        yt_video=YouTube(str(url))
        streams=yt_video.streams.filter(only_audio=True)
        stream=streams.first()
        stream.download(filename="auidio.mp4")
        audio_file= open("auidio.mp4", "rb")
        transcript = openai.Audio.transcribe("whisper-1",audio_file)
        st.info(transcript["text"])

    if st.button("Summarize"):
        yt_video=YouTube(str(url))
        streams=yt_video.streams.filter(only_audio=True)
        stream=streams.first()
        stream.download(filename="auidio.mp4")
        audio_file= open("auidio.mp4", "rb")
        transcript = openai.Audio.transcribe("whisper-1",audio_file)
        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="Please summarize this article in a few points (points should be in 1,2,3,..): " + transcript["text"],
                max_tokens=516,
                temperature=0.5
            )
        res = response["choices"][0]["text"]
        st.info(res)


def text_to_image():
    st.title("Text to Image")
    inp=st.text_input("Enter Text")

    if st.button("Generate"):
        response = openai.Image.create(
            prompt=inp,
            n=1,
            size="256x256"
        )   
        image_url = response['data'][0]['url']
        st.image(image_url, caption=inp)

def main():
    navbar = """
    <style>
        .navbar {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
            padding: 20px;
            margin-bottom: 20px;
        }
        .navbar-title {
            font-size: 24px;
            font-weight: bold;
            margin-right: 10px;
        }
        .navbar-logo {
            height: 40px;
        }
    </style>
    
    <div class="navbar">
        <div class="navbar-title">SummifyNow</div>
        <img class="navbar-logo" src="https://t4.ftcdn.net/jpg/00/90/86/81/360_F_90868187_CNzU7oaUJ0GG4voml6QBzX7EQJIaaLod.jpg" alt="Logo">
    </div>
    """
    st.markdown(navbar, unsafe_allow_html=True)

    navbar = st.sidebar
    navbar.title("Navigation")
    page = navbar.radio("Go to", ("Summarize Written Text", "Summarize Audio", "Summarize YouTube Video", "Convert text to Image",))

    if page == "Summarize Written Text":
        summarize_written_text()
    elif page == "Summarize Audio":
        summarize_audio()
    elif page == "Summarize YouTube Video":
        summarize_youtube_video()
    elif page=="Convert text to Image":
        text_to_image()

if __name__ == "__main__":
    main()
