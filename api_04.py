import requests
import json
import time
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES
import pprint
import nltk
nltk.download('punkt')
import nltk.data


transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
headers_assemblyai = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

# listennotes_episode_endpoint = 'https://listen-api.listennotes.com/api/v2/episodes'
# headers_listennotes = {
#   'X-ListenAPI-Key': API_KEY_LISTENNOTES,
# }


# def get_episode_audio_url(episode_id):
#     url = listennotes_episode_endpoint + '/' + episode_id
#     response = requests.request('GET', url, headers=headers_listennotes)

#     data = response.json()
#     # pprint.pprint(data)

#     episode_title = data['title']
#     thumbnail = data['thumbnail']
#     podcast_title = data['podcast']['title']
#     audio_url = data['audio']
#     return audio_url, thumbnail, podcast_title, episode_title

def transcribe(audio_url, auto_chapters, speaker_labels):
    transcript_request = {
        'audio_url': audio_url,
        'auto_chapters': auto_chapters,
        "speaker_labels": speaker_labels
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers_assemblyai)
    pprint.pprint(transcript_response.json())
    return transcript_response.json()['id']


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers_assemblyai)
    return polling_response.json()
    


def get_transcription_result_url(url, auto_chapters, speaker_labels):
    transcribe_id = transcribe(url, auto_chapters, speaker_labels)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']

        print("waiting for 60 seconds")
        time.sleep(60)
            

def save_transcript(audio_url):
    #audio_url, thumbnail, podcast_title, episode_title = get_episode_audio_url(episode_id)
    episode_id = audio_url.split('/')[-1]

    data, error = get_transcription_result_url(audio_url, auto_chapters=True, speaker_labels=True)
    if data:
        filename = episode_id + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
        
        filename = episode_id + 'convo.txt'
        with open(filename, 'w') as f:
            convo = data['utterances']
            for sp in convo:
                f.write("Speaker " + sp['speaker']+": ")
                f.write(sp['text']+'\n\n')

        filename = episode_id + '_chapters.json'
        with open(filename, 'w') as f:
            chapters = data['chapters']

            data = {'chapters': chapters}
            # data['audio_url']=audio_url
            # data['thumbnail']=thumbnail
            # data['podcast_title']=podcast_title
            # data['episode_title']=episode_title
            # # for key, value in kwargs.items():
            # #     data[key] = value

            json.dump(data, f, indent=4)
            print('Transcript saved')
            return True
    elif error:
        print("Error!!!", error)
        return False


def chuncks(data_1,chunck_size=500,chunck_limit=200):
  tokens=[]
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  s=""
  for i in tokenizer.tokenize(data_1):
    tokens.append(i)
  k=0
  stamp=0
  paras=[]
  while(stamp<len(tokens)):
    # stamp=0
    length=0
    text=""
    k+=1
    while(length<chunck_size and stamp<len(tokens)):
      length+=len(tokens[stamp].split(" "))
      text+=tokens[stamp]
      stamp+=1
    if length>chunck_limit:
      paras.append(text)
    else: paras[len(paras)-1]+=text
    s+="This is the length of chunck -"+str(k)+" Chunck size :"+str(len(text.split(" ")))+"\n\n"
    s+="Text : "+text+"\n\n"
  for i in paras:
    print(len(i.split(" ")))
  
  print(s)
  return (paras,s)


# tokens
