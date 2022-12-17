import streamlit as st
import glob
import json
from api_04 import save_transcript,chuncks

st.title("Podcast Summarization")
st.header("Summary of full convo and convo script")

ch = st.sidebar.selectbox("Source", options=["url", 'upload', 'sample_podcast_url'])
url=""
button = False
if ch=='sample_podcast_url':
    st.write("Copy and Paste one of these urls")
    st.write("https://av.voanews.com/clips/LERE/2013/12/29/a66e301f-9419-44e0-9e37-9af125dfc8cd.mp3")
    st.write("https://av.voanews.com/clips/LERE/2013/12/01/10794ca3-b4cc-45be-9a34-2677d4fbbf71.mp3")
    st.write("https://av.voanews.com/clips/VLE/2022/02/02/cf3cfe62-d3e9-4166-81b2-a5909ca52a1e_hq.mp3")


elif ch == 'upload':
    url = st.write("Upload functionality will be implemented in the next release! Please enter remote files only!!")

else:
    url = st.sidebar.text_input("Enter remote url:")
    button = st.sidebar.button("Summary", on_click=save_transcript, args=(url,))

def get_clean_time(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
        
    return start_t


if button:
    episode_id = url.split('/')[-1]

    filename = episode_id + '_chapters.json'
    filename1 = episode_id + '.txt'
    filename2 = episode_id + 'convo.txt'

    print(filename1)

    print(filename)
    with open(filename, 'r') as f:
        data = json.load(f)

    with open(filename1, 'r') as f:
        text = f.read()
    
    with open(filename2, 'r') as f:
        convos = f.read()

    chapters = data['chapters']

    # episode_title = data['episode_title']
    # thumbnail = data['thumbnail']
    # podcast_title = data['podcast_title']
    # audio = data['audio_url']

    # st.header(f"{podcast_title} - {episode_title}")
    # st.image(thumbnail, width=200)
    # st.markdown(f'#### {episode_title}')

    for chp in chapters:
        with st.expander(chp['gist'] + ' - ' + get_clean_time(chp['start'])):
            chp['summary']

    expander1 = st.expander("## Raw text ##")
    expander1.write(text)
    
    
    chuncks_text,chunck_paras=chuncks(text,chunck_size=500)
    expander2 = st.expander("## Chuncks ##")
    expander2.write(chunck_paras)


    expander3 = st.expander("## Conversation ##")
    expander3.write(convos)



    # _ = st.sidebar.download_button("download", data=data, file_name="output.json")

