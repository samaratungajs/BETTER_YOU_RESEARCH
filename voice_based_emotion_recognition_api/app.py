
from flask import Flask, render_template, request, redirect,jsonify
import librosa
import random
import json

import soundfile
import os,glob,pickle

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import  MLPClassifier
from sklearn.metrics import accuracy_score
import os
import pandas as pd
import librosa
import glob 
import pyaudio
import wave


app = Flask(__name__)
# loading json and creating model
from keras.models import model_from_json
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")
print("Loaded model from disk")
 

#Extract features(mfcc,chroma,mel) from a sound file
def extract_feature(file_name,mfcc,chroma,mel):
  with soundfile.SoundFile(file_name) as sound_file:
    X=sound_file.read(dtype='float32')
    sample_rate=sound_file.samplerate
    if chroma:
      stft=np.abs(librosa.stft(X))
    result=np.array([])
    if mfcc:
      mfccs=np.mean(librosa.feature.mfcc(y=X,sr=sample_rate,n_mfcc=40).T,axis=0)
      result=np.hstack((result,mfccs))
    if chroma:
      chroma=np.mean(librosa.feature.chroma_stft(S=stft,sr=sample_rate).T,axis=0)
      result=np.hstack((result,chroma))
    if mel:
      mel=np.mean(librosa.feature.melspectrogram(X,sr=sample_rate).T,axis=0)
      resutl=np.hstack((result,mel))
  return result

emotions = {
    0 : 'Female_angry',
    1 : 'Female_calm',
    2 : 'Female_fearful',
    3 : 'Female_happy',
    4 : 'Female_sad',
    5 : 'male_angry',
    6 : 'male_calm',
    7 : 'male_fearful',
    8 : 'male_happy',  
    9 : 'male_sad'
}
emo_list = list(emotions.values())



@app.route("/", methods=["GET", "POST"])
def home():
     return render_template('index.html')


@app.route("/predict", methods=["POST"])


def predict():
     print("hello")
     #get audio file and save it

     audio=request.files['audio']
    

  
    #  audio_file = request.files['audio_file']
    #  file_name=str(random.randint(0,100000))
    #  audio_file.save(file_name)

    #  #livedf= pd.DataFrame(columns=['feature'])
    #  audio='OAF_bath_disgust.wav'

    #invoke keyword spotting service
    #  kss=keyword_Spotting_service()

    #  predicted_keyword=kss.predict(file_name)

    #  os.remove(file_name)

    #  data={"keyword",predicted_keyword}
    #  return jsonify(data)
   
     X, sample_rate = librosa.load(audio, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
     sample_rate = np.array(sample_rate)
     mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
     featurelive = mfccs
     livedf2 = featurelive
     livedf2= pd.DataFrame(data=livedf2)
     livedf2 = livedf2.stack().to_frame().T
     twodim= np.expand_dims(livedf2, axis=2)
     livepreds = loaded_model.predict(twodim, batch_size=32,  verbose=1)
     livepreds1=livepreds.argmax(axis=1)
     pred_np = np.squeeze(np.array(livepreds).tolist(), axis=0) 
     liveabc = livepreds1.astype(int).flatten()
    #  if liveabc == 0: prediction="Female_angry"
    #  elif liveabc == 1:prediction="Female Calm"
    #  elif liveabc == 2:prediction="Female Fearful"
    #  elif liveabc == 3:prediction="Female Happy"
    #  elif liveabc == 4:prediction="Female Sad"
    #  elif liveabc == 5:prediction="Male Angry"
    #  elif liveabc == 6:prediction="Male calm"
    #  elif liveabc == 7:prediction="Male Fearful"
    #  elif liveabc == 8:prediction="Male Happy"
    #  elif liveabc == 9:prediction="Male sad"

     res = {}
     mylist=list(pred_np)
     round_to_whole = [round(num,2) for num in mylist]
     for key in emo_list:
        for value in round_to_whole:
           res[key] = value
           round_to_whole.remove(value)
           break
 
# Printing resultant dictionary
    
    #  print("Resultant dictionary is : " + str(res))

     res1={}
     print(list(list(res.items())[0]))
     mylist=list(pred_np)
     round_to_whole = [round(num,3) for num in mylist]
     print(round_to_whole)
     for keys, value in res.items():
       key1='angry'
       value1=round_to_whole[0]+round_to_whole[5]
       res1={key1:value1}

       key2='calm'
       value2=round_to_whole[1]+round_to_whole[6]
       res1.update({key2:value2})

       key3='fearful'
       value3=round_to_whole[2]+round_to_whole[7]
       res1.update({key3:value3})

       key4='happy'
       value4=round_to_whole[3]+round_to_whole[8]
       res1.update({key4:value4})

       key5='sad'
       value5=round_to_whole[4]+round_to_whole[5]
       res1.update({key5:value5})


   # if('angry' in keys):
   #    key1='angry'
   #    value1=value[0]+value[5]
   #    res1.add(key1,value1)

     prediction=json.dumps(res1)
     print(res1) 

     return prediction
     return render_template('index.html', **locals())


if __name__ == "__main__":
    app.run(debug=True, threaded=True)