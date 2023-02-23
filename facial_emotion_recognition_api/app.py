import os
import glob
import cv2
import numpy as np
from cv2 import CAP_ANY, CAP_DSHOW
from flask import Flask, Response, redirect, render_template, request, url_for
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

#load model  
model = model_from_json(open("model.json", "r").read())  

#load weights  
model.load_weights('model.h5')  


face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  

UPLOAD_FOLDER = 'video'
ALLOWED_EXTENSIONS = {'mp4'}


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/gen_frames',methods=["POST"])
def gen_frames(): 

    file = request.files['file'] # Gives Content type text/html etc
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return 'success'

    list_of_files = glob.glob('video/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    camera = cv2.VideoCapture(latest_file)


    emo = []


# def gen_frames():  # generate frame by frame from camera
    Angry=0
    Disgust=0
    Fear=0
    Happy=0
    Neutral=0
    Sad=0
    Surprise=0

    while True:
        # Capture frame by frame
        success, frame = camera.read()
        if not success:
            break
        else:
            gray_img= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        
            faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)  
            
        
            for (x,y,w,h) in faces_detected:
                print('WORKING')
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),thickness=7)  
                roi_gray=gray_img[y:y+w,x:x+h]          #cropping region of interest i.e. face area from  image  
                roi_gray=cv2.resize(roi_gray,(48,48))  
                img_pixels = image.img_to_array(roi_gray)  
                img_pixels = np.concatenate((img_pixels,)*3, axis = -1)
                img_pixels = np.expand_dims(img_pixels, axis = 0) 
                img_pixels /= 255  
        
                print(img_pixels.shape)
                
                predictions = model.predict(img_pixels)  
        
                #find max indexed array  
                
                max_index = np.argmax(predictions[0])
                mx=max(max(predictions))
  
        
                emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']  
                predicted_emotion = emotions[max_index] 
                
                print(predicted_emotion)

                        
                if(predicted_emotion == 'neutral' ):
                    Neutral = Neutral+mx
                    emo.append((predicted_emotion,Neutral))
                elif(predicted_emotion == 'angry' ):
                    Angry = Angry+mx
                    emo.append((predicted_emotion,Angry))
                elif(predicted_emotion == 'disgusted' ):
                    Disgust = Disgust+mx
                    emo.append((predicted_emotion,Disgust))
                elif(predicted_emotion == 'fearful' ):
                    Fear = Fear+mx
                    emo.append((predicted_emotion,Fear))
                elif(predicted_emotion == 'happy' ):
                    Happy = Happy+mx
                    emo.append((predicted_emotion,Happy))
                elif(predicted_emotion == 'sad' ):
                    Sad = Sad+mx
                    emo.append((predicted_emotion,Sad))

                elif(predicted_emotion == 'surprised' ):
                    Surprise = Surprise+mx
                    emo.append((predicted_emotion,Surprise))

                        

                cv2.putText(frame, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)  
        
            # resized_img = cv2.resize(frame, (1000, 700))  
            
            # ret, buffer = cv2.imencode('.jpg', frame)
            
            # frame = buffer.tobytes()
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    d = dict(emo)
    return d


    


# @app.route('/video_feed')
# def video_feed():
#     #Video streaming route. Put this in the src attribute of an img tag
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/')
# def index():
#     return render_template('index.html')

# # @app.route('/gen_frames',methods=["POST"])


# @app.route('/emo')
# def emotions():
#     d = dict(emo)
#     print(d)
#     return d

if __name__ == '__main__':
    app.run(port=8080, debug=True)
